class HistoryBuilder:

    def __init__(self):
        pass

    def build_player_history(self, tracks):

        player_histories = {}

        for frame_num, frame_players in enumerate(tracks["players"]):

            for track_id, player in frame_players.items():

                player_histories.setdefault(track_id, []).append({

                    "frame": frame_num,

                    "pitch_x": player["pitch_x"],

                    "pitch_y": player["pitch_y"],

                    "bbox": player["bbox"],

                    "team": player.get("team"),

                    "team_color": player.get("team_color"),

                    "has_ball": player.get("has_ball", False)

                })

        return player_histories

    def build_team_history(self, player_histories):

        team_histories = {}

        for track_id, history in player_histories.items():

            for point in history:
                team = point["team"]

                team_histories.setdefault(team, []).append({

                    "track_id": track_id,

                    **point

                })

        return team_histories