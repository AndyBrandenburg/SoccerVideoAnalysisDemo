import numpy as np
class DistanceAnalyzer:
    def __init__(self):
        pass

    def calculate_distance(self, player_histories):

        player_distances = {}

        for track_id, history in player_histories.items():

            total_distance = 0

            for i in range(1, len(history)):
                previous = history[i - 1]

                current = history[i]

                dx = current["pitch_x"] - previous["pitch_x"]

                dy = current["pitch_y"] - previous["pitch_y"]

                distance = np.sqrt(dx ** 2 + dy ** 2)

                total_distance += distance

            player_distances[track_id] = total_distance

        return {
            "player_distances": player_distances,
        }