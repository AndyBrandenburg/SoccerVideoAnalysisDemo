from ultralytics.solutions import heatmap
import numpy as np
import cv2

class HeatmapMaker:
    def __init__(self):
        pass

    def build_player_heatmap(
            self,
            player_history,
            width,
            height
    ):
        heatmap = np.zeros(
            (height, width),
            dtype=np.float32
        )

        for point in player_history:

            x = int(point["x"])
            y = int(point["y"])

            if 0 <= x < width and 0 <= y < height:
                heatmap[y, x] += 1

        print(
            "Player heatmap points:",
            np.count_nonzero(heatmap)
        )

        heatmap = cv2.GaussianBlur(
            heatmap,
            (101, 101),
            0
        )

        return heatmap



    def build_team_heatmap(self, player_histories, width, height):
        heatmap = np.zeros(
            (height, width),
            dtype=np.float32
        )

        for history in player_histories.values():

            for point in history:

                x = int(point["x"])
                y = int(point["y"])

                if 0 <= x < width and 0 <= y < height:
                    heatmap[y, x] += 1
        #Debugging code
        print("Heatmap points:", np.count_nonzero(heatmap))
        #Implements Blurring for smoother appearance
        heatmap = cv2.GaussianBlur(
            heatmap,
            (101, 101),
            0
        )

        return heatmap

    def save_heatmap(self, heatmap, output_path):
        heatmap_norm = cv2.normalize(
            heatmap,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        heatmap_norm = heatmap_norm.astype(np.uint8)

        heatmap_color = cv2.applyColorMap(
            heatmap_norm,
            cv2.COLORMAP_JET
        )

        cv2.imwrite(
            output_path,
            heatmap_color
        )
