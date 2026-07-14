# Vehicle Damage Detection System

An AI-powered web application for automatic vehicle damage detection using **YOLOv8** and **Streamlit**. The system identifies different types of vehicle damage from uploaded images, estimates repair costs based on detected severity, and generates a detailed inspection report.

---

## Features

* Detects multiple vehicle damage types using a trained YOLOv8 model
* Supports image upload (JPG, JPEG, PNG)
* Adjustable detection confidence threshold
* Damage severity assessment
* Estimated repair cost calculation
* Interactive Streamlit web interface
* Automatic inspection report generation
* Downloadable damage assessment report

---

## Tech Stack

* Python 3.
* Streamlit
* Ultralytics YOLOv8
* OpenCV
* NumPy
* Pillow
* Matplotlib

---

## Project Structure

```text
vehicle_damage_detection/
│
├── app.py                     # Streamlit application
├── requirements.txt           # Project dependencies
├── args.yaml                  # Configuration
│
├── src/
│   ├── detector.py            # YOLO detection module
│   ├── assessment.py          # Damage assessment logic
│   ├── report.py              # Report generation
│   └── config.py              # Project configuration
│
├── notebook/                  # Development notebooks
├── reports/                   # Generated inspection reports
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/your-username/vehicle_damage_detection.git
```

Move into the project folder

```bash
cd vehicle_damage_detection
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## How It Works

1. Upload a vehicle image.
2. Adjust the confidence threshold if required.
3. Run the detection model.
4. Review detected damages and severity.
5. View estimated repair costs.
6. Generate and download the inspection report.

---

## Supported Damage Classes

* Dent
* Scratch
* Crack
* Glass Shatter
* Lamp Broken
* Tire Flat

---

## Supported Image Formats

* JPG
* JPEG
* PNG

---

## Output

The system provides:

* Annotated vehicle image
* Detected damage locations
* Damage class labels
* Confidence scores
* Severity assessment
* Estimated repair cost
* Inspection report

---

## Future Improvements

* Video damage detection
* Real-time webcam support
* Insurance claim integration
* Repair shop recommendations
* Multi-vehicle detection
* Cloud deployment
* Damage history tracking

---
