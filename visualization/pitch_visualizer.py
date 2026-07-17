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

