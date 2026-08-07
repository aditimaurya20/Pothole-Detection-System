# Pothole Detection System

A web-based computer vision application that detects road potholes from images, videos, and live webcam streams using the YOLOv8 object detection model. The project integrates deep learning with the Django framework to provide an interactive interface for real-time pothole detection.

---

## Overview

Road surface defects such as potholes contribute significantly to vehicle damage and road safety issues. This project demonstrates how deep learning can be applied to automate pothole detection, reducing the need for manual inspection.

The application enables users to upload images or videos, or use a live webcam feed, and returns the processed output with detected potholes highlighted using bounding boxes.

---

## Key Features

- Detect potholes in uploaded images
- Detect potholes in uploaded videos
- Real-time pothole detection using a webcam
- Bounding box visualization with confidence scores
- Web-based interface built with Django
- YOLOv8-powered object detection
- OpenCV-based image and video processing

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Backend Framework | Django |
| Computer Vision | OpenCV |
| Deep Learning | Ultralytics YOLOv8 |
| Frontend | HTML, CSS |

---

## Project Structure

```
Pothole-Detection-System/
│
├── detector/                 # Django application
├── pothole_project/          # Django project configuration
├── .gitignore
├── data.yaml                 # Dataset configuration
├── image.jpeg                # Sample input image
├── manage.py
├── requirements.txt
├── train.py                  # Model training script
├── test.py                   # Detection script
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/aditimaurya20/Pothole-Detection-System.git
```

### Navigate to the project directory

```bash
cd Pothole-Detection-System
```

### Create a virtual environment (Recommended)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install the required dependencies

```bash
pip install -r requirements.txt
```

### Start the Django development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Usage

### Image Detection

- Upload an image through the web interface.
- The application processes the image and highlights detected potholes.

### Video Detection

- Upload a video file.
- Each frame is analyzed using the trained detection model.
- The processed video is generated with detected potholes highlighted.

### Live Detection

- Launch the live detection module.
- The application accesses the webcam and performs real-time pothole detection.

---

## Detection Model

The project uses **YOLOv8 (You Only Look Once Version 8)** for object detection.

YOLOv8 provides fast inference while maintaining high detection accuracy, making it suitable for real-time computer vision applications.

---

## Future Enhancements

Potential improvements include:

- GPS-based pothole location tracking
- Severity classification of road damage
- Integration with cloud storage
- REST API support
- Mobile application integration
- Automatic road maintenance reporting

---

## Author

**Aditi Maurya**

GitHub: https://github.com/aditimaurya20

---

## License

This project is intended for educational and learning purposes.
