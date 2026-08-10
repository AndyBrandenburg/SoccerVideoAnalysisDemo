# Soccer Video Analysis Platform

Developer: Andrew Brandenburg

Piedra Alta Sistemas

# About This Project:

This sports analysis platform takes a short soccer video clip and uses Ultralytics YOLO and ByteTrack to detect objects like players, referees, and the ball. It provides analysis features like convex hulls (Polygons showing team shapes and formations), heatmaps, trajectories, and more analytics both on a 2D pitch view and an overlay on the original video. It also collects and exports JSON data and stores information in SQL Lite and SQL Server databases.

This platform was built to provide professional analysis from soccer match clips and answer questions that many coaches and soccer clubs often ask like formations, player histories, player trajectories, ball control, team zones, and more which can be used to provide analysis and answers to professional questions.

## Getting Started

### Prerequisites

- Python 3.14.0+
- Ultralytics YOLO v11.0
- Supervision 0.28.0+

### Installation
1. **Clone the repository:**
```bash
   git clone https://github.com/AndyBrandenburg/SoccerVideoAnalysisDemo.git
   ```
2. **Navigate into the project folder:**
   ```bash
   cd SoccerVideoAnalysisDemo.git
   ```

3. **Install all required packages:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: If you are using PyCharm, you can simply open the project folder and click the "Install requirements" popup bar).*

4. **Run the program**

    *For Streamlit Usage:*
    ```bash
   streamlit run streamlit_app.py
   ```
   
    *For Running the Main:*
    ```bash
   python main.py
   ```
