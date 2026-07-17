class TouchAnalyzer:
    def __init__(self):
        self.team_frames = {}
        self.player_frames = {}
        self.previous_owner = None

    def calculate_touches(self, tracks):
        touches = {}
        team_frames = {}
        player_frames = {}
        total_frames = 0
        previous_owner = None

        for frame_num, frame_players in enumerate(tracks["players"]):
            current_owner = None

            for track_id, player in frame_players.items():

                if player.get("has_ball", False):
                    current_owner = track_id

                    break

            if current_owner is not None:

                if current_owner != previous_owner:

                    if current_owner not in touches:
                        touches[current_owner] = 0

                    touches[current_owner] += 1

                previous_owner = current_owner

        return {
            "player_touches": touches,
            "total_touches": sum(touches.values())
        }

