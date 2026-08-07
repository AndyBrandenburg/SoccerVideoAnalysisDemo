
from visualization.pitch_visualizer import PitchVisualizer
from analytics.team_zone_analyzer import TeamZoneAnalyzer
from analytics.heatmaps import HeatmapAnalyzer
from visualization.overlay_visualizer import OverlayVisualizer
class TacticalVisualizer:
    def __init__(self):
        self.pitch_visualizer = PitchVisualizer()

        self.zone_analyzer = TeamZoneAnalyzer()
        self.heatmap_maker = HeatmapAnalyzer()
        self.overlay_visualizer = OverlayVisualizer()

    def build_zone_video(self, tracks, video_frames):
        output_frames = []

        for frame_num, (frame_players,
                        frame_referees,
                        frame_ball) in enumerate(
            zip(
                tracks["players"],
                tracks["referees"],
                tracks["ball"]
            )
        ):
            pitch = self.pitch_visualizer.create_pitch()

            #-------Players------
            pitch = self.pitch_visualizer.draw_players(
                pitch,
                frame_players
            )
            #-------Referees-------
            pitch = self.pitch_visualizer.draw_referees(
                pitch,
                frame_referees
            )
            #-------Ball-------
            pitch = self.pitch_visualizer.draw_ball(
                pitch,
                frame_ball
            )

            #-------Team Hulls-------
            hulls = self.zone_analyzer.calculate_frame_team_hulls(

                frame_players

            )
            pitch = self.pitch_visualizer.draw_team_hulls(

                pitch,

                hulls

            )
            #-------Team Centers-------
            centers = self.zone_analyzer.calculate_frame_team_centers(

                frame_players
            )
            #-------Team zones-------
            pitch = self.pitch_visualizer.draw_team_centers(

                pitch,
                centers

            )
            output_frames.append(pitch)

        return output_frames

    def build_pitch_video(self, tracks, video_frames):
        output_pitch_frames = []
        for frame_num, (frame_players,
                        frame_referees,
                        frame_ball) in enumerate(
            zip(
                tracks["players"],
                tracks["referees"],
                tracks["ball"]
            )
        ):
            pitch = self.pitch_visualizer.create_pitch()

            # -------Players------
            pitch = self.pitch_visualizer.draw_players(
                pitch,
                frame_players
            )
            # -------Referees-------
            pitch = self.pitch_visualizer.draw_referees(
                pitch,
                frame_referees
            )
            # -------Ball-------
            pitch = self.pitch_visualizer.draw_ball(
                pitch,
                frame_ball
            )
            output_pitch_frames.append(pitch)
        return output_pitch_frames

    def build_heatmap_video(self, tracks, video_frames):

        output_frames = []

        for frame_num in range(len(video_frames)):
            pitch = self.pitch_visualizer.create_pitch()

            frame_players = tracks["players"][frame_num]

            team_heatmap = self.heatmap_maker.calculate_frame_team_heatmap(
                frame_players
            )
            pitch = self.pitch_visualizer.draw_team_heatmaps(
                pitch,
                team_heatmap
            )

            pitch = self.pitch_visualizer.draw_players(
                pitch,
                frame_players
            )

            pitch = self.pitch_visualizer.draw_referees(
                pitch,
                tracks["referees"][frame_num]
            )

            pitch = self.pitch_visualizer.draw_ball(
                pitch,
                tracks["ball"][frame_num]
            )

            output_frames.append(pitch)
        return output_frames

    ##-----OVERLAY HULL VIDEO BUILDER-----##
    def build_overlay_hull_video(
            self,
            tracks,
            video_frames
    ):

        output_frames = []

        for frame_num, frame_players in enumerate(
                tracks["players"]
        ):
            # Copy the original video frame
            frame = video_frames[frame_num].copy()

            # Calculate hulls for this frame
            team_hulls = self.zone_analyzer.calculate_overlay_team_hulls(
                frame_players
            )

            # Draw hulls onto the original frame
            frame = self.overlay_visualizer.draw_team_hulls(
                frame,
                team_hulls
            )

            output_frames.append(frame)

        return output_frames

    def build_overlay_heatmap_video(
            self,
            tracks,
            video_frames
    ):

        output_frames = []

        for frame_num, frame_players in enumerate(
                tracks["players"]
        ):
            frame = video_frames[frame_num].copy()

            team_heatmaps = (
                self.heatmap_maker.calculate_frame_team_heatmap(
                    frame_players
                )
            )
            frame = self.overlay_visualizer.draw_players(
                frame,
                frame_players
            )

            frame = self.overlay_visualizer.draw_team_heatmaps(
                frame,
                team_heatmaps
            )

            output_frames.append(frame)

        return output_frames

