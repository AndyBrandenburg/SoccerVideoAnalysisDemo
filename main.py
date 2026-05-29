from utils.video_utils import read_video, save_video
from trackers import Tracker
import cv2
import os
import numpy as np
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner

def main():
    # Read video
    video_path = 'Video_Input/Soccer_Video1.mp4'

    video_frames, fps = read_video(video_path)
    print("FPS:", fps)

    # Create unique stub file name per video
    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    stub_path = f"stubs/{video_name}_tracks.pkl"


    #Initialize the tracker
    tracker = Tracker('models/best.pt')

    tracks = tracker.get_object_tracker(video_frames,
                                        read_from_stub=True,
                                        stub_path= stub_path)

    # Interpolate ball positions
    tracks['ball'] = tracker.interpolate_ball_positions(tracks["ball"])

    # Assign player teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0],
                                    tracks['players'][0])

    # Loop over each player and assign them to correct team
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num],
                                                 track['bbox'],
                                                 player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

    # Assign ball acquisition
    player_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        if assigned_player != -1:
            team_ball_control.append(team)

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

    print("video frames:", len(video_frames))
    print("player tracks:", len(tracks["players"]))
    print("ball tracks:", len(tracks["ball"]))
    print("ref tracks:", len(tracks["referees"]))
    print("team ball control:", len(team_ball_control))
    #Draw output
    ##Draw Object Tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)

    print("Input frames:", len(video_frames))
    print("Output frames:", len(output_video_frames))

    #Save Video
    save_video(
        output_video_frames,
        'output_videos/output_video_test1.avi',
        fps
    )


if __name__ == '__main__':
    main()