import numpy as np
class DistanceAnalyzer:
    def __init__(self):
        pass

    def calculate_distance(self, tracks):

        player_distance = {}
        team_distance = {}

        player_histories = {}

        # ----------------------------
        # Build player histories
        # ----------------------------
        for frame_players in tracks["players"]:

            for track_id, player in frame_players.items():
                player_histories.setdefault(track_id, []).append({

                    "pitch_x": player["pitch_x"],

                    "pitch_y": player["pitch_y"],

                    "team": player.get("team")

                })

        # ----------------------------
        # Calculate each player's distance
        # ----------------------------
        for track_id, history in player_histories.items():

            total_distance = 0

            for i in range(len(history) - 1):
                p1 = history[i]
                p2 = history[i + 1]

                dx = p2["pitch_x"] - p1["pitch_x"]
                dy = p2["pitch_y"] - p1["pitch_y"]

                distance = np.sqrt(
                    dx ** 2 +
                    dy ** 2
                )

                total_distance += distance

            player_distance[track_id] = total_distance

        # ----------------------------
        # Sum by team
        # ----------------------------
        for track_id, history in player_histories.items():
            team = history[0]["team"]

            team_distance.setdefault(team, 0)

            team_distance[team] += player_distance[track_id]

        return {

            "player_distance": player_distance,

            "team_distance": team_distance

        }