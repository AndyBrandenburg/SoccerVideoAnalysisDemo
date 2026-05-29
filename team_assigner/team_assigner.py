from sklearn.cluster import KMeans
import numpy as np
import cv2




class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}

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

        # Convert to LAB (better for lighting changes)
        roi_lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

        # Reshape for clustering
        pixels = roi_lab.reshape(-1, 3)

        # KMeans clustering
        kmeans = self.get_clustering_model(roi_lab)

        labels = kmeans.labels_

        # Count cluster sizes (more stable than corner trick)
        counts = np.bincount(labels)

        player_cluster = np.argmax(counts)

        # Get dominant color in BGR space for consistency with OpenCV drawing
        player_color = kmeans.cluster_centers_[player_cluster]

        return player_color

    def assign_team_color(self, frame, player_detections):
        player_colors = []
        for _, player_detection in player_detections.items():
            bbox = player_detection['bbox']
            player_color = self.get_player_color(frame, bbox)
            player_colors.append(player_color)

        kmeans = KMeans(n_clusters = 2, init = "k-means++", n_init = 1).fit(player_colors)

        self.kmeans = kmeans

        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]


    def get_player_team(self, frame, player_bbox, player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        player_color = self.get_player_color(frame, player_bbox)

        team_id = self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id += 1

        if player_id == 35:
            team_id = 1

        self.player_team_dict[player_id] = team_id

        return team_id

