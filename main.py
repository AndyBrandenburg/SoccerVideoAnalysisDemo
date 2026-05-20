from utils.video_utils import read_video, save_video
from trackers import Tracker

def main():
    #Read video
    video_frames, fps = read_video(
        'Video_Input/Soccer_Test_Video.mp4'
    )
    print("FPS:", fps)

    #Initialize the tracker
    tracker = Tracker('models/best.pt')

    tracks = tracker.get_object_tracker(video_frames,
                                        read_from_stub=True,
                                        stub_path='stubs/track_stubs.pkl')

    #Draw output
    ##Draw Object Tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks)

    print("Input frames:", len(video_frames))
    print("Output frames:", len(output_video_frames))

    #Save Video
    save_video(
        output_video_frames,
        'output_videos/output_video.avi',
        fps
    )


if __name__ == '__main__':
    main()