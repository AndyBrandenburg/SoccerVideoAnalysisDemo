class Position_Generator:
    def __init__(self):
        pass

    def collect_player_positions(self, tracks):

        player_positions = {}

        for frame_players in tracks["players"]:

            for track_id, player in frame_players.items():
                player_positions.setdefault(track_id, []).append({

                    "pitch_x": player["pitch_x"],

                    "pitch_y": player["pitch_y"],

                    "team": player.get("team"),

                    "team_color": player.get("team_color")
                })

        return player_positions

    def calculate_average_positions(self, player_positions):

        average_positions = {}

        for track_id, positions in player_positions.items():

            total_x = 0
            total_y = 0

            for point in positions:
                total_x += point["pitch_x"]
                total_y += point["pitch_y"]

            average_positions[track_id] = {

                "pitch_x": total_x / len(positions),

                "pitch_y": total_y / len(positions),

                "team": positions[0]["team"],

                "team_color": positions[0]["team_color"]

            }

        return average_positions
