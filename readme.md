# Water surface garbage detection system

## Project Introduction

The water surface garbage detection system is an intelligent monitoring tool based on computer vision technology, using the YOLOv11 object detection algorithm. It supports two modes of real-time monitoring through cameras or video file analysis, automatically identifying and classifying water surface garbage, and helping environmental workers efficiently deal with water pollution problems.

The system can accurately identify multiple types of common waste such as kitchen waste, recyclable waste, and electronic waste, and output real-time detection results (including waste name, type, confidence level, and area level). It also supports recording the detection process, providing data support for water ecological governance.


## Core functions

|Functional module | Specific description|
|----------|----------|
|Dual mode detection | Supports two modes of "real-time camera detection" and "video file upload analysis", suitable for different usage scenarios|
|Intelligent garbage recognition | Based on YOLOv11 algorithm, it identifies 20+common types of garbage and automatically classifies them into kitchen waste, recyclable, electronic, and other garbage|
|Visualization result display | Dual window comparison display of "original image" and "detection annotation image", with clear display of garbage information in annotation boxes and text|
|Test result table | Real time generated structured table displaying garbage names, types, confidence levels, and area levels for easy data recording and analysis|
|Screen cropping | Supports custom cropping detection area (0-1 normalized range), focusing on the core monitoring area to reduce interference|
|Video recording | Original and detection images can be recorded (in MP4 format), with files named after timestamps for easy backtracking in the future|
|Progress tracking | Display real-time progress bar during video file detection to intuitively understand processing progress|


## Technology Stack
- **Front end framework**: Streamlit (Quickly build web interfaces, support real-time interaction)
- Computer Vision: OpenCV (Image Processing), YOLOv11 (Object Detection, Implemented by Ultralytics)
- **Programming Language**: Python 3.8+
- **Dependency Management**: IP (Python Package Management Tool)


## Environment construction

### 1. Hardware requirements

-Basic configuration: CPU i5+/8GB memory (supports video file analysis)
-Recommended configuration: GPU NVIDIA GTX 1650+(supports real-time camera detection, requires CUDA installation)


### 2. Software dependency installation
1. Clone the project locally (or download the source code):
```bash
Git clone<project repository address>
CD water surface garbage detection system
```

2. Install dependency packages:
```bash
#Basic dependencies (CPU version)
pip install streamlit opencv-python numpy ultralytics

#If using GPU acceleration (CUDA 11.8+needs to be installed first)
pip install streamlit opencv-python numpy ultralytics torch torchvision torchaudio --index-url  https://download.pytorch.org/whl/cu118
```


### 3. Model preparation
The system automatically downloads the YOLOv11 nano pre trained model by default (lightweight, fast, suitable for real-time detection), without the need for manual download.   
If you need to use a custom training model, you can place the model file (such as ` custom_yolov51. pt `) in the project root directory and specify the model path in ` detector. py `:
```python
#Detectability. py initialization method modification
def __init__(self, model_path="custom_yolov11.pt", confidence_threshold=0.1):
# . .. Original code ..
```

## Project Structure
```
Water surface garbage detection system/
∝ - app. py # Main application entrance (interface interaction, logic control)
∝ - detector. py # Detection core module (YOLOv11 call, garbage classification, result drawing)
∝ - README.md # Project Description Document
∝ - origina_xxxx.mp4 # Recorded original video (automatically generated, named by timestamp)
└ - processed_xxxx.mp4 # Recorded detection video (automatically generated, named by timestamp)
```


## Usage tutorial

### 1. Start the system
Execute the following command in the root directory of the project to start the Streamlinet application:
```bash
streamlit run app.py
```
After execution, the browser will automatically open (default address:` http://localhost:8501 `Go to the system homepage.

### 2. Select detection mode
The system provides two tab pages, corresponding to two detection modes:


#### Mode 1: Real time detection by camera

1. In the "Camera Detection" tab, select the available cameras (the system automatically detects connected cameras).
2. (Optional) Adjust the "Crop Region": Use the slider to set the left/upper/right/lower boundaries (0-1 range), focusing on the core monitoring area.
3. (Optional) Check "Record Video": When enabled, it will generate two video files: the original image and the detection image (saved in the project root directory).
4. Click the "Start" button to activate the camera and perform real-time detection. The dual window displays the "Original Screen" and "Detection Screen".
During the detection process, you can click the "Freeze Screen" button to pause the detection, or click the "Stop" button to end the detection.
6. The detection result table will be updated in real-time, displaying the garbage information identified in the current frame.


### #Mode 2: Video File Analysis

1. On the "Video File Detection" tab, click on "Upload Video" and select a video file in MP4/AVI/MOV/MKV format.
2. (Optional) Adjust the "Crop Area": In the same camera mode, focus on the core area.
3. (Optional) Check "Record Video": Once enabled, save the video of the detection process.
4. Click the "Start" button, the system will start analyzing the video, and the progress bar will display the processing progress.
After the video processing is completed, the system will prompt "Video processing completed", and you can view the historical detection result table.


###  3. Result Description

The test result table contains the following fields:

- Garbage name: The specific category of garbage identified (such as "bottle", "banana").
- Garbage type: Classification results (kitchen waste, recyclable waste, electronic waste, other waste).
- Confidence: Recognition accuracy (0-1, higher values are more reliable, default threshold is 0.1).
- * Area level**: The size of garbage relative to the image (L1: area ≤ 5%, L2: area>5%).

## Frequently Asked Questions

### 1. After startup, it prompts' No available cameras detected '
- Check if the camera is connected to the computer (USB camera needs to be securely plugged in).
- Close other applications that occupy the camera (such as Zoom, WeChat Video).
- If using the built-in camera in the laptop, make sure it is not disabled by the system.

###  2. Slow detection speed (stuttering)
-Switch to CPU lightweight mode: Ensure to use the 'yolo11n. pt' model (default) and avoid using large models (such as' yolo11n.pt').
-Reduce video resolution: Modify the video save resolution in app. py (default 640x480).
-Enable GPU acceleration: Install CUDA and use the GPU version PyTorch (refer to step 2 of "Environment setup").

### 3. Recording video without output
-Check the root directory permissions of the project: Ensure that the current user has write permission (Windows needs to run the terminal as an administrator, Linux/MacOS can execute 'chmod 755.' to grant permission).
-Confirm that 'Record Video' is checked: Only by clicking 'Start' after checking it will the recording file be generated.

###  4. Low accuracy of garbage recognition
-Adjust the confidence threshold: Increase the confidence threshold in 'detector. py' (e.g. from 0.1 to 0.3) to filter out low confidence results.
-Use custom model: retrain YOLOv11 based on the surface garbage dataset and replace the default model.
-Optimize shooting environment: Ensure sufficient lighting to avoid blurry images or garbage being obstructed.

## System Introduction
This water surface garbage detection system is based on computer vision technology, aiming to solve the problems of low efficiency and high labor costs in water surface garbage monitoring. Core advantages of the system:
1. **Efficient real-time**: YOLOv11 algorithm supports detection at over 30 frames per second, meeting real-time monitoring requirements.
2. Multi class recognition: covering 20+types of waste in four categories: kitchen waste, recyclables, electronics, and others, suitable for complex water environments.
3. **Strong usability**: No professional technical background is required, and detection operations can be completed through a visual interface.
4. **Data Traceability**: Supports video recording and result table export, facilitating subsequent data analysis and report generation.

We are committed to supporting environmental protection through technological innovation and providing efficient and intelligent solutions for water ecological governance.


## Contact Information
If you have any questions or suggestions, you can contact us through the following methods:
-Developer email:< your-email@example.com >
-Project Warehouse:< https://github.com/your-username/ Surface Garbage Detection System>(Example Address)