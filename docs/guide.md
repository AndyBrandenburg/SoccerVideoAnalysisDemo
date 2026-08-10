# How to use this application (step-by-step guide)

## The Prerequisites:
1. Make sure Ultralytics YOLO v11 (yolo11l.pt) and Supervision 0.28.0+ are installed. This is the foundation of the object tracking used in this platform.
2. Make sure to either train the model using a roboflow dataset or have training files (best.pt) installed for a more advanced, smoother model.
3. Make sure all the python packages necessary are installed (requirements.txt has them all).

## The main program:
1. The first steps are shown in the README file, but here's the commands to run:\
*For Streamlit Usage:*
    ```bash
   streamlit run streamlit_app.py
   ```
   
    *For Running the Main:*
    ```bash
   python main.py
   ```
2. Once inside the StreamLit interface, click the button that says "Upload" and select the video file you want to use.
3. On the left hand side of the interface, you will see a checkbox list of different outputs you can select, select whatever outputs you like.

4. Now click the "Analyze Video" button, now the program is running and processing the video. This step might take a while to analyze everything. The longer the video, the longer it will take.
5. Once the video is done, there will be two sections that appear below. One is a tab list of each output video you selected, you can download these videos by clicking the download button below them. The other section is for the exports. This is where you can see the JSON nad database data and download them.

