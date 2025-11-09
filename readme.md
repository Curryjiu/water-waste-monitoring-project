# Aqua AI - Water Surface Garbage Detection System

## Project Introduction

The Water Surface Garbage Detection System is an intelligent monitoring tool based on computer vision technology, utilizing the YOLOv11 object detection algorithm. It supports two modes: real-time monitoring via cameras and video file analysis. The system can automatically identify and classify water surface garbage, helping environmental workers efficiently address water pollution issues.

The system can accurately recognize various common waste types such as kitchen waste, recyclables, and electronic waste, outputting real-time detection results (including garbage name, type, confidence level, and area grade). It also supports recording the detection process, providing data support for water ecological governance.

## Core Features

| Feature Module | Description |
|----------------|-------------|
| Dual-mode Detection | Supports "real-time camera detection" and "video file upload analysis" modes to adapt to different usage scenarios |
| Intelligent Garbage Recognition | Based on the YOLOv11 algorithm, identifies over 20 common garbage types and automatically classifies them into kitchen waste, recyclables, electronic waste, and other waste |
| Visual Result Display | Dual-window comparison of "original image" and "detection annotated image", clearly showing garbage information through bounding boxes and text |
| Detection Result Table | Generates real-time structured tables displaying garbage name, type, confidence, and area grade for easy data recording and analysis |
| Image Cropping | Supports custom cropping of detection areas (0-1 normalized range) to focus on core monitoring areas and reduce interference |
| Video Recording | Can record original and detected images (MP4 format), with files named by timestamp for easy subsequent review |
| History Record Management | Saves detection history data, supporting queries by time, location, garbage type, etc. |
| Map Visualization | Marks garbage detection locations on a map, supporting viewing of image information at historical detection points |

## System Architecture

- **Frontend Layer**: Web interface built with Bootstrap, providing functional modules such as real-time detection, history records, and map view
- **Application Layer**: Flask backend framework handling HTTP requests, video stream transmission, and business logic
- **Algorithm Layer**: YOLOv11 object detection algorithm for garbage recognition and classification
- **Data Layer**: SQLite database storing detection records, location information, and image data

## Technology Stack

- **Frontend Framework**: Bootstrap 5, JavaScript (real-time refresh and interaction)
- **Backend Framework**: Flask (Python Web framework)
- **Computer Vision**: OpenCV (image processing), YOLOv11 (object detection, implemented via Ultralytics)
- **Programming Language**: Python 3.8+
- **Database**: SQLite (lightweight data storage)
- **Map Service**: Amap API (location visualization)
- **Dependency Management**: Python package management tool (pip)

## Environment Setup

### 1. Hardware Requirements

- Basic Configuration: CPU i5+/8GB RAM (supports video file analysis)
- Recommended Configuration: NVIDIA GTX 1650+ GPU (supports real-time camera detection, requires CUDA installation)

### 2. Software Dependency Installation

1. Clone the project to local (or download source code):
```bash
git clone <project repository URL>
cd water-surface-garbage-detection-system
```

2. Install dependency packages:
```bash
# Basic dependencies (CPU version)
pip install streamlit opencv-python numpy ultralytics flask geopy

# For GPU acceleration (requires CUDA 11.8+ installed first)
pip install streamlit opencv-python numpy ultralytics flask geopy torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. Model Preparation

The system automatically downloads the YOLOv11 nano pre-trained model by default (lightweight, fast speed, suitable for real-time detection), no manual download required.

To use a custom trained model, place the model file (e.g., `custom_yolov11.pt`) in the project root directory and specify the model path in `detector.py`:
```python
# Modify initialization method in detector.py
def __init__(self, model_path="custom_yolov11.pt", confidence_threshold=0.1):
# ... original code ...
```

## Project Structure

```
water-surface-garbage-detection-system/
├── app.py # Main application entry (Flask service, route management, business logic)
├── camera.py # Video capture related functions
├── deepseek.py # Code for interacting with Deepseek API
├── detector.py # Core detection module (YOLOv11 call, garbage classification, result drawing)
├── detection.db # Database for storing detection data
├── yolo11n.pt # YOLOv11 nano model file
├── yolo11m.pt # YOLOv11 medium model file
├── templates/ # Frontend template files
│   ├── base.html # Base template
│   ├── index.html # Real-time detection page
│   ├── history.html # History records page
│   ├── map.html # Map view page
│   └── main.html # Main interface template
├── uploads/ # Directory for storing uploaded files
├── screenshots/ # Directory for storing screenshots
└── README.md # Project description document
```

## Usage Tutorial

### 1. Starting the System

Execute the following command in the project root directory to start the application:
```bash
python app.py
```
After execution, the browser will automatically open (default address: `http://localhost:5000`) to enter the system homepage.

### 2. Selecting Detection Mode

The system provides two tabs corresponding to two detection modes:

#### Mode 1: Real-time Camera Detection

1. In the "Camera Detection" tab, select an available camera (the system automatically detects connected cameras)
2. (Optional) Adjust the "Crop Area": Use sliders to set left/top/right/bottom boundaries (0-1 range) to focus on the core monitoring area
3. (Optional) Check "Record Video": When enabled, two video files (original image and detected image) will be generated (saved in the project root directory)
4. Click the "Start" button to activate the camera and perform real-time detection, with dual windows displaying "Original Image" and "Detection Image"
5. During detection, you can click the "Freeze Frame" button to pause detection or the "Stop" button to end detection
6. The detection result table will update in real-time, showing garbage information identified in the current frame

#### Mode 2: Video File Analysis

1. In the "Video File Detection" tab, click "Upload Video" and select a video file in MP4/AVI/MOV/MKV format
2. (Optional) Adjust the "Crop Area": Same as camera mode, focusing on the core area
3. (Optional) Check "Record Video": When enabled, saves the detection process video
4. Click the "Start" button, and the system will start analyzing the video, with a progress bar showing the processing progress
5. After video processing is complete, the system will prompt "Video processing completed", and you can view the historical detection result table

### 3. Result Explanation

The detection result table contains the following fields:

- Garbage Name: Specific category of identified garbage (e.g., "bottle", "banana peel")
- Garbage Type: Classification result (kitchen waste, recyclables, electronic waste, other waste)
- Confidence: Recognition accuracy (0-1, higher values are more reliable, default threshold is 0.1)
- Area Grade: Size of garbage relative to the image (L1: area ≤ 5%, L2: area > 5%)

### 4. Other Features

- **History Records**: Click "Detection History" in the navigation bar to view all detection records, including time, location, garbage type, and detection images
- **Map View**: Click "Map View" to see the distribution of historical detection points on a map; click markers to view corresponding detection images

## Frequently Asked Questions

### 1. "No available cameras detected" prompt after startup

- Check if the camera is connected to the computer (USB cameras need to be securely plugged in)
- Close other applications using the camera (such as Zoom, WeChat Video)
- If using a laptop's built-in camera, ensure it is not disabled by the system

### 2. Slow detection speed (stuttering)

- Switch to CPU lightweight mode: Ensure using the `yolo11n.pt` model (default) and avoid using large models
- Reduce video resolution: Modify the video save resolution in app.py (default 640x480)
- Enable GPU acceleration: Install CUDA and use GPU version PyTorch (refer to step 2 of "Environment Setup")

### 3. No output when recording video

- Check project root directory permissions: Ensure the current user has write permissions (Windows needs to run the terminal as administrator; Linux/MacOS can execute `chmod 755 .` to grant permissions)
- Confirm "Record Video" is checked: Recording files are only generated when clicking "Start" after checking this option

### 4. Low garbage recognition accuracy

- Adjust confidence threshold: Increase the confidence threshold in `detector.py` (e.g., from 0.1 to 0.3) to filter out low-confidence results
- Use custom model: Retrain YOLOv11 based on water surface garbage datasets and replace the default model
- Optimize shooting environment: Ensure sufficient lighting, avoid blurry images or obscured garbage

## System Features

1. **Efficient Real-time Performance**: YOLOv11 algorithm supports detection speeds above 30 frames per second, meeting real-time monitoring needs
2. **Multi-class Recognition**: Covers over 20 waste types in four categories (kitchen, recyclables, electronic, other), adapting to complex water environments
3. **User-friendly**: No professional technical background required; detection operations can be completed through a visual interface
4. **Data Traceability**: Supports video recording and result table export, facilitating subsequent data analysis and report generation

## Contact Information

If you have any questions or suggestions, please contact us through:
- Developer Email: <Curryjiu@example.com>
- Project Repository: <https://github.com/Curryjiu/water-waste-monitoring-project>