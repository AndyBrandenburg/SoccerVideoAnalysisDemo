from sklearn.cluster import KMeans
import numpy as np
import cv2


#Team Assigner

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}
        self.player_team_history = {}
        self.player_colors_history = {}

    def get_clustering_model(self,image):
        # Reshape image into 2d array
        image_2d = image.reshape(-1, 3)

        kmeans = KMeans(
            n_clusters=2,
            init="k-means++",
            n_init=10
        ).fit(image_2d)

        return kmeans
    def get_player_color(self, frame, bbox):
        x1, y1, x2, y2 = map(int, bbox)

        # Crop player
        image = frame[y1:y2, x1:x2]

        # Safety check (avoid empty crops)
        if image.size == 0:
            return None

        h, w = image.shape[:2]

        # Focus on torso region (more stable than full bbox / top half)
        roi = image[
            int(h * 0.2):int(h * 0.6),
            int(w * 0.3):int(w * 0.7)
        ]
        if roi.size == 0:
            return None

        # Convert to LAB (better for lighting changes)
        roi_lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)


        # KMeans clustering
        kmeans = self.get_clustering_model(roi_lab)

        labels = kmeans.labels_

        # Count cluster sizes (more stable than corner trick)
        counts = np.bincount(labels)

        player_cluster = np.argmax(counts)

        # Get dominant color in BGR space for consistency with OpenCV drawing
        player_color = kmeans.cluster_centers_[player_cluster]

        return player_color

    # def assign_team_color(self, frame, player_detections):
    #     player_colors = []
    #     for _, player_detection in player_detections.items():
    #         bbox = player_detection['bbox']
    #         player_color = self.get_player_color(frame, bbox)
    #         player_colors.append(player_color)
    #
    #     print("player_colors:", len(player_colors))
    #
    #     if len(player_colors) < 2:
    #         print("Not enough players for team assignment")
    #         return
    #
    #     kmeans = KMeans(n_clusters = 2, init = "k-means++", n_init = 1).fit(player_colors)
    #
    #     self.kmeans = kmeans
    #
    #     self.team_colors[1] = kmeans.cluster_centers_[0]
    #     self.team_colors[2] = kmeans.cluster_centers_[1]

    def assign_team_color_from_colors(self, player_colors):
        player_colors = [
            c for c in player_colors
            if c is not None and len(c) == 3
        ]

        if len(player_colors) < 10:
            print("Not enough data for stable team clustering")
            return

        kmeans = KMeans(n_clusters=2, n_init=10)
        kmeans.fit(player_colors)

        self.kmeans = kmeans

        self.team_colors = {
            1: kmeans.cluster_centers_[0],
            2: kmeans.cluster_centers_[1]
        }
    def get_player_team(self, frame, bbox, player_id):

        # 1. If we already assigned this player before, reuse it
        if player_id in self.player_team_history:
            return self.player_team_history[player_id]

        # 2. Make sure KMeans exists before using it
        if not hasattr(self, "kmeans"):
            return 0  # unknown team fallback

        # 3. Extract player color
        player_color = self.get_player_color(frame, bbox)

        # 4. Safety check (invalid crop etc.)
        if player_color is None:
            return 0

        # 5. Predict team using trained KMeans
        team_id = self.kmeans.predict(player_color.reshape(1, -1))[0] + 1

        # 6. Store result so player stays consistent across frames
        self.player_team_history[player_id] = team_id

        return team_id
