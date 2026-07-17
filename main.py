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
from homography.homography import HomographyGenerator
from exporters.json_exporter import export_tracking_json
from visualization import pitch_visualizer
from visualization.pitch_visualizer import PitchVisualizer
from analytics.positioning import Position_Generator
from analytics.possession_analyzer import PossessionAnalyzer
from analytics.touch_analyzer import TouchAnalyzer
from analytics.distance_analyzer import DistanceAnalyzer

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

    # Match_analysis dictionary
    match_analysis = {}

    image_points = [
        [174, 914],
        [1752, 901],
        [1456, 182],
        [432, 205]
    ]

    field_points = [
        [0, 68],
        [105, 68],
        [105, 0],
        [0, 0]
    ]

    # Homography
    homography = HomographyGenerator()

    homography.set_points(
        image_points,
        field_points
    )

    homography.compute_homography()

    tracks = homography.transform_tracks(tracks)


    first_frame = tracks["players"][0]

    for track_id, player in first_frame.items():
        print(f"Player {track_id}")

        print("Image:",
              player["bbox"])

        print("Pitch:",
              player["pitch_x"],
              player["pitch_y"])

        print("----------------")




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
                    match_id,
                    player["pitch_x"],
                    player["pitch_y"]
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
                    match_id,
                    ball_dict[1]["pitch_x"],
                    ball_dict[1]["pitch_y"]
                )
    sqlite_db.save()
    sqlserver_db.save()

    sqlite_db.close()
    sqlserver_db.close()



    player_histories = build_player_histories(
        tracks
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
    PITCH_WIDTH = 1050
    PITCH_HEIGHT = 680

    # heatmap_width = video_frames[0].shape[1]
    # heatmap_height = video_frames[0].shape[0]
    #Debugging code
    for item in player_histories[1][:5]:
        print("-----------------PLAYER_HISTORIES_ITEM----------------------")
        print(item)

    player_heatmap = heatmap_maker.build_player_heatmap(
        player_histories[1],
        PITCH_WIDTH,
        PITCH_HEIGHT
    )
    team_heatmap = heatmap_maker.build_team_heatmap(
        player_histories,
        PITCH_WIDTH,
        PITCH_HEIGHT
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

    for frame_ball in tracks["ball"]:

        if 1 not in frame_ball:
            continue

        ball = frame_ball[1]

        bbox = ball["bbox"]

        image_x = (bbox[0] + bbox[2]) / 2
        image_y = (bbox[1] + bbox[3]) / 2

        pitch_x, pitch_y = homography.transform_homography(
            image_x,
            image_y
        )

        ball["pitch_x"] = pitch_x
        ball["pitch_y"] = pitch_y

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


    # Possession analysis
    print("-----CHECK FOR FRAMES WITH POSSESSION-----")
    for player_id, player in tracks["players"][0].items():
        print(player)
    possession_analyzer = PossessionAnalyzer()

    possession_data = possession_analyzer.calculate_possession(
        tracks
    )
    print(possession_data)

    match_analysis["possessions"] = possession_data

    #Touch analysis
    print("-----TOUCH ANALYSIS FOR PLAYERS-----")
    for player_id, player in tracks["players"][0].items():
        print(player)
    touch_analyzer = TouchAnalyzer()
    touch_data = touch_analyzer.calculate_touches(
        tracks)
    print(touch_data)

    match_analysis["touches"] = touch_data

    #JSON implementation

    print("JSON TEST")
    print(tracks["players"][0][1])

    export_tracking_json(
        tracks,
        "JSON_data/tracking_output.json"
    )


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

    # Get average position
    position_generator = Position_Generator()
    print("TEST PLAYER")
    print(tracks["players"][0][1])
    player_positions = position_generator.collect_player_positions(
        tracks
    )
    average_positions = position_generator.calculate_average_positions(
        player_positions
    )
    match_analysis["average_positions"] = average_positions

    # print("---DEBUGGING---")
    # for track_id, position in average_positions.items():
    #
    #     print(track_id, position)
    #
    #     if track_id >= 5:
    #         break

    # Pitch Visualization
    pitch_visualizer = PitchVisualizer()
    output_pitch_frames = []
    print("---BALL TRACKS---")
    print(tracks["ball"][0])

    for frame_num in range(len(video_frames)):
        pitch = pitch_visualizer.create_pitch()

        pitch = pitch_visualizer.draw_players(
            pitch,
            tracks["players"][frame_num]
        )
        pitch = pitch_visualizer.draw_referees(
            pitch,
            tracks["referees"][frame_num]
        )

        pitch = pitch_visualizer.draw_ball(
            pitch,
            tracks["ball"][frame_num]
        )

        output_pitch_frames.append(pitch)

    len(output_pitch_frames)
    print("-----PITCH FRAMES-----")
    print(type(output_pitch_frames))
    print(len(output_pitch_frames))
    print(output_pitch_frames[0])

    #Output for average positions:
    average_pitch = pitch_visualizer.create_pitch()

    print("MATCH ANALYSIS:")
    print(match_analysis)

    print("MATCH ANALYSIS KEYS:")
    print(match_analysis.keys())
    average_pitch = pitch_visualizer.draw_average_positions(
        average_pitch,
        match_analysis["average_positions"]
    )

    #Distance Analyzer
    distance_analyzer = DistanceAnalyzer()
    distance_results = distance_analyzer.calculate_distance(
        tracks
    )
    match_analysis["distance"] = distance_results


    cv2.imwrite(
        "assets/average_positions.png",
        average_pitch
    )

    save_video(
        output_pitch_frames,
        "output_videos/pitch_view_trails.avi",
        fps
    )

    # cv2.imwrite(
    #     "assets/pitch_test.png",
    #     pitch
    # )

    #Save Video
    save_video(
        output_video_frames,
        'output_videos/output_video_test_homography.avi',
        fps
    )


if __name__ == '__main__':
    main()