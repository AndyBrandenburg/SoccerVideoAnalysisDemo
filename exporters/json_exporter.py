import json
import numpy as np


def json_converter(obj):
    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    raise TypeError(
        f"Object of type {type(obj)} "
        f"is not JSON serializable"
    )

def export_tracking_json(tracks, output_path):

    tracking_export = []

    for frame_num in range(len(tracks["players"])):

        frame_data = {
            "frame": frame_num,
            "players": [],
            "referees": [],
            "ball": None
        }

        # Players
        for track_id, player in tracks["players"][frame_num].items():

            frame_data["players"].append({

                "track_id": track_id,

                "bbox": player["bbox"],

                "pitch_x": player.get("pitch_x"),

                "pitch_y": player.get("pitch_y"),

                "team": int(player["team"]) if player.get("team") is not None else None,

                "team_color": (
                    player["team_color"].tolist()
                    if player.get("team_color") is not None
                    else None
                ),

                "has_ball": player.get("has_ball", False)
            })

        # Referees
        for track_id, referee in tracks["referees"][frame_num].items():

            frame_data["referees"].append({

                "track_id": track_id,

                "bbox": referee["bbox"]
            })

        # Ball
        if 1 in tracks["ball"][frame_num]:

            ball = tracks["ball"][frame_num][1]

            frame_data["ball"] = {

                "bbox": ball["bbox"],

                "pitch_x": ball.get("pitch_x"),

                "pitch_y": ball.get("pitch_y")
            }

        tracking_export.append(frame_data)

    with open(output_path, "w") as f:
        json.dump(
            tracking_export,
            f,
            indent=4,
            default=json_converter
        )

    print("JSON WRITE COMPLETE")