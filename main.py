from utils.video_utils import read_video, save_video
from trackers import Tracker
import cv2
import os
import numpy as np
from team_assigner import TeamAssigner
from sklearn.cluster import KMeans
from player_ball_assigner import PlayerBallAssigner
from utils.tracking_data import  load_tracking_data
from analytics.player_histories import build_player_histories
from camera_motion.camera_motion import CameraMotionEstimator
from database.sql_lite import SQLiteManager
from database.sql_server import SQLServerManager
from analytics.heatmaps import  HeatmapMaker

# Main
def collect_player_colors(
        tracks,
        video_frames,
        team_assigner,
        min_colors=20):

    player_colors = []

    for frame_num, players in enumerate(tracks["players"]):

        if len(players) == 0:
            continue

        frame = video_frames[frame_num]

        for _, player in players.items():
            bbox = player["bbox"]

            color = team_assigner.get_player_color(
                frame,
                bbox
            )

            player_colors.append(color)

        if len(player_colors) >= min_colors:
            break

    return player_colors

def main():
    print("STEP 1 - entering main")
    # Read video
    video_path = 'Video_Input/Soccer_Test_Video.mp4'

    video_frames, fps = read_video(video_path)
    print("FPS:", fps)

    print("STEP 2 - video loaded")

    # Create unique stub file name per video
    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    stub_path = f"stubs/{video_name}_tracks.pkl"


    #Initialize the tracker
    tracker = Tracker('models/best (2).pt')
    print("STEP 3 - tracker initialized")

    tracks = tracker.get_object_tracker(video_frames,
                                        read_from_stub=False,
                                        stub_path= stub_path)

    print("Players in frame 0:", len(tracks["players"][0]))
    print("STEP 4 - tracking complete")

    #Implement SQL Lite database:
    # Create database (SQL Lite)
    sqlite_db = SQLiteManager()

    # Create database (SQL Server)
    sqlserver_db = SQLServerManager()

    #Create match
    print(type(fps))
    print(fps)
    match_id = sqlserver_db.create_match(
        video_name=video_path,
        fps=fps,
        width=1920,
        height=1080,
    )


    # Create tables
    sqlite_db.create_tables()

    #Insert Players
    databases = [
        sqlite_db,
        sqlserver_db
    ]

    for frame_num, player_dict in enumerate(tracks["players"]):

        for track_id, player in player_dict.items():

            for db in databases:
                db.insert_player(
                    frame_num,
                    track_id,
                    player["bbox"],
                    match_id
                )

    #Insert Ball
    databases = [
        sqlite_db,
        sqlserver_db
    ]

    for frame_num, ball_dict in enumerate(tracks["ball"]):

        if 1 in ball_dict:

            for db in databases:
                db.insert_ball(
                    frame_num,
                    ball_dict[1]["bbox"],
                    match_id
                )
    sqlite_db.save()
    sqlserver_db.save()

    sqlite_db.close()
    sqlserver_db.close()

    #JSON Implementation
    tracking_data = load_tracking_data(
        "JSON_data/tracking_output.json"
    )

    print("Frames in JSON:", len(tracking_data))
    print(tracking_data[0])

    player_histories = build_player_histories(
        tracking_data
    )
    print(
        "Tracked players:",
        len(player_histories)
    )


    print(
        "Player 1 samples:",
        player_histories[1][:5]
    )

    #Uses the code in heatmaps/HeatmapMaker to build the player heatmap
    heatmap_maker = HeatmapMaker()

    heatmap_width = video_frames[0].shape[1]
    heatmap_height = video_frames[0].shape[0]
    #Debugging code
    for item in player_histories[1][:5]:
        print("-----------------PLAYER_HISTORIES_ITEM----------------------")
        print(item)

    player_heatmap = heatmap_maker.build_player_heatmap(
        player_histories[1],
        heatmap_width,
        heatmap_height
    )
    team_heatmap = heatmap_maker.build_team_heatmap(
        player_histories,
        1920,
        1080
    )

    heatmap_maker.save_heatmap(
        team_heatmap,
        "output_heatmaps/team_heatmap_low.png"
    )

    heatmap_maker.save_heatmap(
        player_heatmap,
        "output_heatmaps/player1_heatmap_low.png"
    )

    # Interpolate ball positions
    print("BALL FRAME 0:", tracks["ball"][0])
    print("BALL FRAME 1:", tracks["ball"][1])
    print("BALL FRAME 2:", tracks["ball"][2])
    tracks['ball'] = tracker.interpolate_ball_positions(tracks["ball"])

    # Assign player teams
    team_assigner = TeamAssigner()

    player_colors = collect_player_colors(
        tracks,
        video_frames,
        team_assigner
    )

    print("Collected colors:", len(player_colors))

    if len(player_colors) < 5:
        print("Not enough data for team clustering")
        return

    team_assigner.assign_team_color_from_colors(player_colors)

    # max_players = max(len(players) for players in tracks["players"])
    # print("Maximum players detected in a frame:", max_players)
    #
    # all_player_colors = []
    #
    # for frame_num, players in enumerate(tracks["players"]):
    #     if len(players) >= 2:
    #         for _, player in players.items():
    #             bbox = player["bbox"]
    #             color = team_assigner.get_player_color(video_frames[frame_num], bbox)
    #             all_player_colors.append(color)
    #
    #     if len(all_player_colors) >= 10:
    #         break
    #
    # team_assigner.kmeans = KMeans(n_clusters=2, n_init=10).fit(all_player_colors)
    #
    # team_assigner.team_colors = {
    #     1: team_assigner.kmeans.cluster_centers_[0],
    #     2: team_assigner.kmeans.cluster_centers_[1],
    # }


    print("Team colors:", team_assigner.team_colors)

    # Loop over each player and assign them to correct team
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num],
                                                 track['bbox'],
                                                 player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            # tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]
            tracks['players'][frame_num][player_id]['team_color'] = (
                team_assigner.team_colors.get(team, (0, 0, 255))
            )

    # Assign ball acquisition
    player_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num].get(1, {}).get('bbox', None)

        if ball_bbox is None:
            team_ball_control.append(team_ball_control[-1] if team_ball_control else 0)
            continue
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            player_team = player_track[assigned_player]['team']
            team_ball_control.append(player_team)

        else:
            if len(team_ball_control) > 0:
                team_ball_control.append(team_ball_control[-1])
            else:
                team_ball_control.append(0)
    team_ball_control = np.array(team_ball_control)



    # #Save cropped image of a player
    # for track_id, player in tracks['players'][0].items():
    #     bbox = player['bbox']
    #     frame = video_frames[0]
    #
    #     # Crop bbox from frame
    #     cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
    #
    #     # Save the cropped image
    #     cv2.imwrite(f'output_videos/cropped_image.jpg', cropped_image)
    #     break

    # print("video frames:", len(video_frames))
    # print("player tracks:", len(tracks["players"]))
    # print("ball tracks:", len(tracks["ball"]))
    # print("ref tracks:", len(tracks["referees"]))
    # print("team ball control:", len(team_ball_control))
    #Draw output
    ##Draw Object Tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)

    print("Input frames:", len(video_frames))
    print("Output frames:", len(output_video_frames))

    #Save Video
    save_video(
        output_video_frames,
        'output_videos/output_video_test_low_trails.avi',
        fps
    )


if __name__ == '__main__':
    main()