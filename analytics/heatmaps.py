from collections import defaultdict, deque
import numpy as np
import cv2

class HeatmapAnalyzer:

    def __init__(
            self,
            grid_width=40,
            grid_height=25,
            history_length = 600
    ):

        self.grid_width = grid_width
        self.grid_height = grid_height

        self.pitch_length = 105
        self.pitch_width = 68


        self.history_length = history_length

        self.team_history = defaultdict(
            lambda: deque(
                maxlen=self.history_length
            )
        )



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
                (31,31),
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

    def calculate_frame_team_heatmap(self, frame_players):


        for track_id, player in frame_players.items():
            team = player["team"]

            self.team_history[team].append({

                "pitch_x": player["pitch_x"],

                "pitch_y": player["pitch_y"],

                "team_color": player["team_color"]

            })

        frame_heatmaps = {}

        for team, history in self.team_history.items():

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
                    cv2.circle(
                        heatmap,
                        (int(grid_x), int(grid_y)),
                        2,
                        float(1.0),
                        -1
                    )

            # blur for smoothing
            heatmap = cv2.GaussianBlur(
                heatmap,
                (31, 31),
                0
            )

            #Normalize
            if np.max(heatmap) > 0:
                heatmap = heatmap / np.max(heatmap)

            # Return the heatmap info in the dict
            frame_heatmaps[team] = {

                "heatmap": heatmap,

                "team_color": history[-1]["team_color"]

            }


        return frame_heatmaps

