import numpy as np
import cv2
class TeamZoneAnalyzer:
    def __init__(self):
        pass

    # def collect_team_positions(self, player_histories):
    #     team_positions = {}
    #
    #     for track_id, history in player_histories.items():
    #
    #         for point in history:
    #             team = point["team"]
    #
    #             team_positions.setdefault(
    #                 team,
    #                 []
    #             ).append({
    #
    #                 "pitch_x": point["pitch_x"],
    #
    #                 "pitch_y": point["pitch_y"],
    #
    #                 "track_id": track_id,
    #
    #                 "frame": point["frame"],
    #
    #                 "team_color": point["team_color"]
    #
    #             })
    #
    #     return team_positions


    def calculate_team_centers(self, team_histories):

        team_centers = {}

        for team, history in team_histories.items():

            total_x = 0
            total_y = 0

            for point in history:

                total_x += point["pitch_x"]
                total_y += point["pitch_y"]

            team_centers[team] = {

                "pitch_x": total_x / len(history),

                "pitch_y": total_y / len(history),

                "team_color": history[0]["team_color"]

            }

        return team_centers

    def calculate_convex_hulls(self, team_histories):
        team_hulls = {}

        for team, history in team_histories.items():
            points = []
            for point in history:
                points.append([
                    point["pitch_x"],
                    point["pitch_y"]
                ])

            points = np.array(
                points,
                dtype=np.float32
            )
            hull = cv2.convexHull(points)

            team_hulls[team] = {

                "hull": hull,

                "team_color": history[0]["team_color"]

            }

        return team_hulls
