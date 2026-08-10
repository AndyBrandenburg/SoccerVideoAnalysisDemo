## Summary for Soccer Video Analysis Demo

This is my project for analyzing soccer videos and analyzing them using Ultralytics YOLO and Supervision Bytetrack to detect the objects inside the video like players, referees, and the ball. This platform takes these detections and creates detailed analysis and stores information in JSON and databases. This platform uses StreamLit to connect to the main and run the program and produce the outputs and results.

## This platform can:

- Analyze player, referee, and ball positions and movements
- Generate 2D pitch overlay maps showing the match in a 2D birds-eye view
- Generate heatmaps and convex hulls (team shape polygons) on the 2D pitch map and overlaid on top of the original video
- Export JSON data of the match
- Store player and match data inside SQL Lite and SQL Server databases which can answer questions coaches and clubs normally ask like:
  - Determining which players are the most utilized in the match using possession and trajectory data
  - Determine average formations of each team using average positions of each player
  - Showing statistics like possession and team ball control which can tell coaches if their schemes are working and how to change them if not
  - Determining each player's role/position using movement history
  - Determining how much offense/defense each team has played so far using data like touches, posession, and movement history
- And much more!


## Document Directory

Explore the inside of this platform:
- [System Architecture](architecture.md)
- [Setup Guide](guide.md)
- [API Reference and Complete List of Classes and Methods](api_reference.md)

