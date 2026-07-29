import cv2
import numpy as np
import os


class PitchVisualizer:

    def __init__(
            self,
            width=1050,
            height=680
    ):
        self.width = width
        self.height = height
        self.track_history = {}

    def create_pitch(self):
        pitch = np.zeros(
            (
                self.height,
                self.width,
                3
            ),
            dtype=np.uint8
        )

        return pitch


    def pitch_to_pixel(
            self,
            pitch_x,
            pitch_y
    ):

        x = int(
            pitch_x *
            self.width /
            105
        )

        y = int(
            pitch_y *
            self.height /
            68
        )

        return x, y

    def draw_trajectory(
            self,
            pitch,
            track_id,
            player,
            color
    ):

        x = int(player["pitch_x"] * self.width / 105)
        y = int(player["pitch_y"] * self.height / 68)

        self.track_history.setdefault(track_id, [])
        self.track_history[track_id].append((x, y))

        self.track_history[track_id] = \
            self.track_history[track_id][-40:]

        history = self.track_history[track_id]

        if len(history) > 1:

            for i in range(1, len(history)):
                cv2.line(
                    pitch,
                    history[i - 1],
                    history[i],
                    color,
                    2
                )

        return pitch

    def draw_players(self, pitch, players):
        for track_id, player in players.items():
            x = int(player["pitch_x"] * self.width / 105)
            y = int(player["pitch_y"] * self.height / 68)

            color = player.get(
                "team_color",
                (0, 255, 0)
            )
            pitch = self.draw_trajectory(
                pitch,
                track_id,
                player,
                color
            )

            cv2.circle(
                pitch,
                (x, y),
                6,
                tuple(int(c) for c in color),
                -1
            )

            cv2.putText(
                pitch,
                str(track_id),
                (x + 8, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                tuple(int(c) for c in color),
                1

            )

        return pitch

    def draw_referees(self, pitch, referees):
        for track_id, referee in referees.items():
            x = int(referee["pitch_x"] * self.width / 105)
            y = int(referee["pitch_y"] * self.height / 68)
            cv2.circle(
                pitch,
                (x, y),
                6,
                (0, 255, 255),
                -1
            )
        return pitch

    def draw_ball(self, pitch, ball):
        for track_id, ball in ball.items():
            x = int(ball["pitch_x"] * self.width / 105)
            y = int(ball["pitch_y"] * self.height / 68)
            cv2.circle(
                pitch,
                (x, y),
                4,
                (255, 255, 255),
                -1
            )
        return pitch

    def draw_average_positions(
            self,
            pitch,
            average_positions
    ):

        for track_id, player in average_positions.items():
            x = int(player["pitch_x"] * self.width / 105)
            y = int(player["pitch_y"] * self.height / 68)

            color = player.get(
                "team_color",
                (0, 255, 0)
            )
            print("---track_id, player---")
            print(track_id, player)

            cv2.circle(
                pitch,
                (x, y),
                12,
                tuple(int(c) for c in color),
                -1
            )

            cv2.circle(
                pitch,
                (x, y),
                12,
                (0, 0, 0),
                2
            )

            cv2.putText(
                pitch,
                str(track_id),
                (x - 6, y + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

        return pitch

    def draw_team_centers(self, pitch, team_centers):
        for team, center in team_centers.items():
            x, y = self.pitch_to_pixel(
                center["pitch_x"],
                center["pitch_y"]
            )

            #Get team color
            color = tuple(
                int(c)
                for c in center["team_color"]
            )

            cv2.circle(
                pitch,
                (x, y),
                20,
                color,
                -1
            )

            cv2.putText(
                pitch,
                f"Team {team}",
                (x - 25, y - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
        return pitch

    def draw_team_hulls(self, pitch, team_hulls):
        for team, data in team_hulls.items():
            hull = data["hull"]

            color = tuple(
                int(c)
                for c in data["team_color"]
            )

            pixel_points = []

            for point in hull:
                x, y = self.pitch_to_pixel(
                    point[0][0],
                    point[0][1]
                )
                pixel_points.append([x, y])

            pixel_points = np.array(
                pixel_points,
                dtype=np.int32
            )

            overlay = pitch.copy()

            cv2.fillPoly(
                overlay,
                [pixel_points],
                color
            )

            cv2.polylines(
                pitch,
                [pixel_points],
                True,
                color,
                3
            )

            cv2.addWeighted(
                overlay,
                0.25,
                pitch,
                0.75,
                0,
                pitch
            )

            center_x = int(np.mean(pixel_points[:, 0]))
            center_y = int(np.mean(pixel_points[:, 1]))

            cv2.putText(
                pitch,
                f"Team {team}",
                (center_x - 20, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
        return pitch

    def draw_team_heatmaps(
            self,
            pitch,
            team_heatmaps
    ):
        for team, data in team_heatmaps.items():
            heatmap = data["heatmap"]

            color = tuple(
                int(c)
                for c in data["team_color"]
            )

            heatmap = cv2.resize(
                heatmap,
                (self.width, self.height),
                interpolation=cv2.INTER_CUBIC
            )

            overlay = np.zeros_like(pitch)
            b, g, r = color
            overlay[:, :, 0] = heatmap * b
            overlay[:, :, 1] = heatmap * g
            overlay[:, :, 2] = heatmap * r

            #Add blend
            cv2.addWeighted(
                overlay,
                0.45,
                pitch,
                0.55,
                0,
                pitch
            )

        return pitch








    def create_pitch_video(self, tracks):

        output_frames = []

        for frame_players in tracks["players"]:
            pitch = self.create_pitch()

            pitch = self.draw_players(
                pitch,
                frame_players
            )

            output_frames.append(pitch)

        return output_frames

