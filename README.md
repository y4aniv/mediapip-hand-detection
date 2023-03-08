# Mediapipe Hand Detection

## Introduction

This code uses the Mediapipe library to detect hands in a video and display the number of hands detected in each frame. It uses a video input given as an argument for hand detection.

## Installation
- Clone this code repository:<br>
```git clone https://github.com/y4aniv/mediapip-hand-detection.git```
- Install dependencies with pip:<br>
```pip install -r requirements.txt```
- Run the program:<br>
```python script.py <video_path.mp4>```

## Functioning
The program uses the OpenCV library to play the video and display the results. The frames are read one by one from the video and sent to the `detect_hands()` function to detect the hands in the frame. The function uses Mediapipe to detect hands and draws the skeleton of each detected hand on the image. The total number of hands detected in the video is also displayed on the screen.

The `detect_hands()` function detects hands in each frame using Mediapipe. It also keeps the position of the hands detected in the previous frame to perform a consistency check and avoid false detections. The hand detection area is defined by the variable `DETECTION_REGION`, and the maximum distance to consider a hand as a false detection is defined by `MAX_DISTANCE`.

## License
This code is licensed under the MIT license. See the `LICENSE` file for more details.
