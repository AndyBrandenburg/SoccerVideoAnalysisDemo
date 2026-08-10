# Architecture

Here is a list of the architecture used in this platform and what it does, what it connects to, and how it contributes to the overall project.

### analytics:
This directory contains all the analyzers in the project that are used for creating analysis features like zones and heatmaps and builds player histories and positions. This is essentially where all the analytics are created before they are drawn in the visualizers and main.

### database:
This directory is responsible for holding the database classes used for connecting the databases to the platform and storing the data.

### exporters:
This is where the JSON data is read and exported.

### JSON_data:
This is the output for the JSON that is exported.

### models:
This is where the training weights are stored, these weights are essential for the program to run as the model is trained using these to make it run better.

### output_videos:
This is where all the videos are output if running this in the IDE.

### player_ball_assigner:
This determines what player has the ball and has possession.

### sports_db:
This is where the SQL Lite database is stored after running the program.

### trackers:
The backbone of the object detection part of the platform. This is where the ByteTrack and YOLO is put to use and the heart of the project. This detects players, assigns them to teams, tracks everything in the video, and sends it to the main. The tracking logic is used in nearly every part of the project in some way from getting the coordinates and history used in the analytics directory to providing all the statistics for the databases.

### Training: 
Inside this directory, you will find the Jupyter notebook used to run the training on the model using a dataset from RoboFlow. This notebook is a general baseline to use if you need to run another training session.

### utils:
This directory contains the basic methods for creating bounding boxes, loading the JSON, and contains the methods for reading and saving the videos that are crucial parts of the main for creating output videos.

### Video_Input:
Directory that stores all the test videos I have used.

### visualization:
One of the most important parts of the platform. This is where the classes and code from the analytics directory are actually drawn and saved. This is where heatmaps, convex hulls, and videos are drawn on a 2D pitch map and an overlay of the original video. The classes and methods from this class are called in the main to save the videos and images generated.

### main:
This is where everything comes together. This is where all the classes and methods are put to use and where the platform runs.


## How these classes go together:
1. Take a video from the Video_Input folder.
2. Then it processes the video frame by frame using the tracker class.
3. While processing the video, it collects things like team colors using player jerseys, who has possession each frame, player positions, and player and ball location.
4. Now it uses this information collected from the tracker to be used in the classes inside the analytics directory, where data like player histories, team formations, and heatmaps are collected.
5. Then it goes to the visualization directory to draw these features like heatmaps and convex hulls, then calls the visualizers to build videos.
6. Then it goes back to main where it uses the save video methods from the utils directory to save the videos/images into the assets or output videos directories, depending on the type.
7. Now everything has finished and the videos/images from the analyzers are output and the data is stored in the JSON and databases.

