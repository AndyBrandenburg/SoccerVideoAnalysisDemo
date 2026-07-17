import cv2
import numpy as np
class HomographyGenerator:
    def __init__(self):
        self.H = None
        self.image_points = None
        self.field_points = None

    def set_points(
            self,
            image_points,
            field_points
    ):
        self.image_points = np.array(
            image_points,
            dtype=np.float32
        )

        self.field_points = np.array(
            field_points,
            dtype=np.float32
        )

    def compute_homography(self):

        self.H, status = cv2.findHomography(
            self.image_points,
            self.field_points
        )

    def get_projection_point(
            self,
            category,
            bbox
    ):

        if category == "ball":
            return (
                (bbox[0] + bbox[2]) / 2,
                (bbox[1] + bbox[3]) / 2
            )

        # Players and referees
        return (
            (bbox[0] + bbox[2]) / 2,
            bbox[3]
        )

    def transform_homography(
            self,
            x,
            y
    ):
        point = np.array(
            [[[x, y]]],
            dtype=np.float32
        )

        transformed = cv2.perspectiveTransform(
            point,
            self.H
        )

        return (
            transformed[0][0][0],
            transformed[0][0][1]
        )

    def transform_tracks(
            self,
            tracks
    ):

        for category in tracks:

            if category not in ["players", "ball", "referees"]:
                continue

            for frame_objects in tracks[category]:

                for track_id, obj in frame_objects.items():
                    image_x, image_y = self.get_projection_point(
                        category,
                        obj["bbox"]
                    )

                    pitch_x, pitch_y = self.transform_homography(
                        image_x,
                        image_y
                    )

                    obj["pitch_x"] = float(pitch_x)
                    obj["pitch_y"] = float(pitch_y)

        return tracks

