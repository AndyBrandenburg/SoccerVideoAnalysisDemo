import cv2
import numpy as np
import os

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS) #Uses cv2 to capture the video
    frames = [] # Initializes frames
    #Uses this loop to analyze the video until there are no more frames to read
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames, fps

def save_video(output_video_frames, output_video_path, fps):
    extension = os.path.splitext(output_video_path)[1].lower()

    if extension == ".mp4":
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    else:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(
        output_video_path,
        fourcc,
        fps,
        (
            output_video_frames[0].shape[1],
            output_video_frames[0].shape[0]
        )
    )
    #write the frame to the video
    for frame in output_video_frames:
        out.write(frame)
    out.release()