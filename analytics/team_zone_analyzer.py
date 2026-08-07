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

    def group_players_by_team(self, frame_players):

        team_positions = {}

        for track_id, player in frame_players.items():

            team = player.get("team")

            if team is None:
                continue

            team_positions.setdefault(team, []).append(player)

        return team_positions

    def calculate_frame_team_centers(self, frame_players):

        team_positions = self.group_players_by_team(frame_players)

        team_centers = {}

        for team, players in team_positions.items():

            total_x = 0
            total_y = 0

            for player in players:
                total_x += player["pitch_x"]
                total_y += player["pitch_y"]

            team_centers[team] = {

                "pitch_x": total_x / len(players),

                "pitch_y": total_y / len(players),

                "team_color": players[0]["team_color"]

            }

        return team_centers

    def calculate_frame_team_hulls(self, frame_players):

        team_positions = self.group_players_by_team(frame_players)

        team_hulls = {}

        for team, players in team_positions.items():

            if len(players) < 3:
                continue

            points = []

            for player in players:
                points.append([

                    player["pitch_x"],
                    player["pitch_y"]

                ])

            points = np.array(
                points,
                dtype=np.float32
            )

            hull = cv2.convexHull(points)

            team_hulls[team] = {

                "hull": hull,
                "team_color": players[0]["team_color"]

            }

        return team_hulls

    def calculate_overlay_team_hulls(self, frame_players):
        team_positions = self.group_players_by_team(frame_players)

        team_overlay_hulls = {}

        for team, players in team_positions.items():

            if len(players) < 3:
                continue

            points = []

            for player in players:
                bbox = player["bbox"]
                center_x = (bbox[0] + bbox[2]) / 2
                bottom_y = bbox[3]

                points.append([
                    center_x,
                    bottom_y
                ])

            points = np.array(
                points,
                dtype=np.float32
            )

            hull = cv2.convexHull(points)

            team_overlay_hulls[team] = {

                "hull": hull,
                "team_color": players[0]["team_color"]

            }

        return team_overlay_hulls
