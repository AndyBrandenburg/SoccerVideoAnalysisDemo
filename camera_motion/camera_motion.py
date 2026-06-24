import cv2
import numpy as np

class CameraMotionEstimator:
    def __init__(self):
        self.total_dx = 0.0
        self.total_dy = 0.0
        self.prev_gray = None

    #Estimate Motion
    def update_camera(self, frame):
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        if self.prev_gray is None:
            self.prev_gray = gray

            return 0, 0

        #Detect Features
        prev_points = cv2.goodFeaturesToTrack(
            self.prev_gray,
            maxCorners=200,
            qualityLevel=0.01,
            minDistance=20
        )
        if prev_points is None:
            self.prev_gray = gray
            return self.total_dx, self.total_dy

        #Track features
        next_points, status, _ = cv2.calcOpticalFlowPyrLK(
            self.prev_gray,
            gray,
            prev_points,
            None
        )

        if next_points is None or status is None:
            self.prev_gray = gray
            return self.total_dx, self.total_dy

        #Keep good matches
        good_old = prev_points[
            status.flatten() == 1
            ]

        good_new = next_points[
            status.flatten() == 1
            ]

        #Compute and accumulate motion
        motion = good_new - good_old
        print("motion shape:", motion.shape)
        print("motion sample:", motion[:5])
        if len(motion) == 0:
            return 0, 0

        motion = motion.reshape(-1, 2)
        dx = np.median(motion[:, 0])
        dy = np.median(motion[:, 1])

        #Debugging code
        print(
            "Frame motion:",
            round(dx, 2),
            round(dy, 2),
            "Total:",
            round(self.total_dx, 2),
            round(self.total_dy, 2)
        )

        self.total_dx += dx
        self.total_dy += dy

        #Save Frame
        self.prev_gray = gray

        return dx, dy
