from ultralytics.solutions import heatmap
import numpy as np
import cv2

class HeatmapAnalyzer:

    def __init__(
            self,
            grid_width=40,
            grid_height=25
    ):

        self.grid_width = grid_width
        self.grid_height = grid_height

        self.pitch_length = 105
        self.pitch_width = 68



    # Build heatmaps for each team

    def calculate_team_heatmaps(
            self,
            team_histories
    ):

        team_heatmaps = {}

        for team, history in team_histories.items():

            heatmap = np.zeros(
                (
                    self.grid_height,
                    self.grid_width
                ),
                dtype=np.float32
            )

            for point in history:

                grid_x = int(
                    point["pitch_x"]
                    * self.grid_width
                    / self.pitch_length
                )

                grid_y = int(
                    point["pitch_y"]
                    * self.grid_height
                    / self.pitch_width
                )

                if (
                    0 <= grid_x < self.grid_width
                    and
                    0 <= grid_y < self.grid_height
                ):

                    heatmap[grid_y, grid_x] += 1

            #blur for smoothing
            heatmap = cv2.GaussianBlur(
                heatmap,
                (5,5),
                0
            )

            if np.max(heatmap) > 0:

                heatmap = heatmap / np.max(heatmap)


            #Return the heatmap info in the dict
            team_heatmaps[team] = {

                "heatmap": heatmap,

                "team_color": history[0]["team_color"]

            }

        return team_heatmaps
