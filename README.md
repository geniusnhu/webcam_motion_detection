Motion Detection with real-time Webcam
By: Hoang Anh Quynh Nhu

----------------------------------------------------------

The engine receives motion and audio from Webcam and process the input frame to detect motion. 
Motion detection is computed based on absolute difference between previous frame and current frame. If the difference exceeds a certain threshold, motion is detected.
Motion Alert is triggered when there are more than a specific number of "Motion" in the sequence.

----------------------------------------------------------

# How to use

1. Clone this repository
2. Create virtual environment
3. Install required packages by `pip install -r requirements.txt`
4. Run bat file **run.bat**

----------------------------------------------------------


Copyright (C) 2024 Hoang Anh Quynh Nhu.
All rights reserved.
