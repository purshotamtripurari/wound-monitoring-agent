🩹 Wound Monitoring Agent

A YOLO-based wound segmentation and monitoring prototype built with Python and Streamlit.

Overview

The Wound Monitoring Agent analyzes uploaded wound images using a trained YOLO segmentation model. It estimates wound area in pixels and compares measurements across multiple observations.

Features

YOLO-based wound segmentation

Upload and analyze multiple wound images

Automatic follow-up dates at seven-day intervals

Wound area measurement in pixels

Observation-to-observation percentage comparison

Progress graph and measurement summary dashboard

Basic image-processing error handling

Technologies Used

Python

Ultralytics YOLO

PyTorch

Streamlit

Pillow

NumPy

Matplotlib

Project Structure

wound-monitoring-agent/
├── app.py
├── agent.py
├── monitoring.py
├── wound_area.py
├── convert_masks.py
├── data.yaml
├── requirements.txt
├── README.md
├── .gitignore
├── models/
│   └── best.pt
└── wound_progress.png

Setup and Installation

Install Python and Git.

Clone or download this repository.

Open a terminal in the project folder.

Install the dependencies:

pip install -r requirements.txt

Ensure the trained model is available at:

models/best.pt

Start the application:

python -m streamlit run app.py

How to Use

Launch the Streamlit application.

Choose the number of observations.

Select the first observation date.

Upload wound images for the available observations.

Click Analyze Wound Progress.

Review the pixel measurements, percentage changes, and progress graph.

Limitations

Measurements are estimates in image pixels, not physical wound area in cm².

Results depend on image quality and model segmentation accuracy.

Changes in lighting, camera angle, distance, and positioning can affect measurements.

A change in measured area alone does not establish wound healing.

Medical Disclaimer

This project is an educational prototype and is not a medical diagnostic device. It does not replace assessment or advice from a qualified healthcare professional.