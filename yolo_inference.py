#import all libraries
from sympy import true
from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "..", "models", "best.pt")

print(model_path)  # helpful for debugging

model = YOLO(model_path)

#Object Detection
results = model.predict(source = "Video_Input/Soccer_Test_Video.mp4", save = True)
print(results[0])
for box in results[0].boxes:
    print(box)


