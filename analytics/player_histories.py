import json
def build_player_histories(tracking_data):

    histories = {}

    for frame_data in tracking_data:

        frame_num = frame_data["frame"]

        for player in frame_data["players"]:

            track_id = player["track_id"]
            bbox = player["bbox"]

            center_x = (bbox[0] + bbox[2]) / 2
            center_y = bbox[3]

            histories.setdefault(track_id, []).append(
                {
                    "frame": frame_num,
                    "x": center_x,
                    "y": center_y
                }
            )

    return histories