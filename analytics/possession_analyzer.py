
class PossessionAnalyzer():
    def __init__(self):
        self.team_frames = {}
        self.player_frames = {}
        self.total_possession_frames = 0

    def calculate_possession(self, tracks):

        team_frames = {}
        player_frames = {}
        total_frames = 0

        # Loop through every frame
        for frame_num, frame_players in enumerate(tracks["players"]):

            # checks to see if there is possession in the frame
            possession_found = False

            # Loop through every player in this frame
            for track_id, player in frame_players.items():


                # Check if player has the ball
                if player.get("has_ball", False):

                    possession_found = True

                    # Get player team
                    team = player.get("team")

                    # -------------------------
                    # Count player possession
                    # -------------------------

                    if track_id not in player_frames:
                        player_frames[track_id] = 0

                    player_frames[track_id] += 1

                    # -------------------------
                    # Count team possession
                    # -------------------------

                    if team not in team_frames:
                        team_frames[team] = 0

                    team_frames[team] += 1

                    # We found the player with the ball
                    # no need to check the rest
                    break

            # Only count frames where possession exists
            if possession_found:
                total_frames += 1

        # Convert counts into percentages

        team_percentages = {}

        for team, frames in team_frames.items():
            team_percentages[team] = (
                                             frames / total_frames
                                     ) * 100

        player_percentages = {}

        for player_id, frames in player_frames.items():
            player_percentages[player_id] = (
                                                    frames / total_frames
                                            ) * 100

        return {
            "team_frames": team_frames,
            "player_frames": player_frames,
            "team_percentages": team_percentages,
            "player_percentages": player_percentages
        }


