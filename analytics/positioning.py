from analytics.history_builder import HistoryBuilder
class Position_Generator:
    def __init__(self):
        pass

    def collect_player_positions(self, tracks):

        player_histories = HistoryBuilder().build_player_history(tracks)

        return player_histories

    def calculate_average_positions(self, player_histories):

        average_positions = {}

        for track_id, history in player_histories.items():

            total_x = 0
            total_y = 0

            for point in history:
                total_x += point["pitch_x"]
                total_y += point["pitch_y"]

            average_positions[track_id] = {

                "pitch_x": total_x / len(history),

                "pitch_y": total_y / len(history),

                "team": history[0]["team"],

                "team_color": history[0]["team_color"]

            }

        return average_positions
