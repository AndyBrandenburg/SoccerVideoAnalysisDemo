class PlayerStatisticsBuilder:
    def __init__(self):
        pass

    def build_player_statistics(self, match_analysis):
        # Pull the analyzer outputs
        average_positions = match_analysis["average_positions"]

        player_touches = \
            match_analysis["touches"]["player_touches"]

        player_distances = \
            match_analysis["distance"]["player_distances"]

        player_possession = \
            match_analysis["possessions"]["player_percentages"]

        player_statistics = {}

        for track_id, player in average_positions.items():
            player_statistics[track_id] = {

                "track_id": int(track_id),

                "team":
                    int(player["team"])
                    if player["team"] is not None
                    else None,

                "team_color": player["team_color"],

                "average_pitch_x":
                    float(player["pitch_x"]),

                "average_pitch_y":
                    float(player["pitch_y"]),

                "touches":
                    int(player_touches.get(track_id, 0)),

                "distance":
                    float(player_distances.get(track_id, 0)),

                "possession":
                    float(player_possession.get(track_id, 0))

            }

        return player_statistics
