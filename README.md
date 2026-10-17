\# 🩹 Wound Monitoring Agent



A YOLO-based wound segmentation and monitoring prototype built with Python and Streamlit.



\## Overview



The Wound Monitoring Agent analyzes uploaded wound images using a trained YOLO segmentation model. It estimates wound area in pixels and compares measurements across multiple observations.



\## Features



\- YOLO-based wound segmentation

\- Upload and analyze multiple wound images

\- Automatic follow-up dates at seven-day intervals

\- Wound area measurement in pixels

\- Observation-to-observation percentage comparison

\- Progress graph and measurement summary dashboard

\- Basic image-processing error handling



\## Technologies Used



\- Python

\- Ultralytics YOLO

\- PyTorch

\- Streamlit

\- Pillow

\- NumPy

\- Matplotlib



\## Project Structure



```text

wound\_monitoring\_agent/

├── app.py

├── agent.py

├── monitoring.py

├── wound\_area.py

├── convert\_masks.py

├── data.yaml

├── requirements.txt

├── README.md

├── .gitignore

└── wound\_progress.png

```



\## Setup and Installation



1\. Install Python.

2\. Clone or download this repository.

3\. Open a terminal in the project folder.

4\. Install the dependencies:



&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



5\. Place the trained model at:



&#x20;  ```text

&#x20;  models/best.pt

&#x20;  ```

models/best.pt

6\. Start the application:



&#x20;  ```bash

&#x20;  python -m streamlit run app.py

&#x20;  ```



\## How to Use



1\. Launch the Streamlit application.

2\. Choose the number of observations.

3\. Select the first observation date.

4\. Upload the wound images for the available observations.

5\. Click \*\*Analyze Wound Progress\*\*.

6\. Review the pixel measurements, percentage changes, and progress graph.



\## Limitations



\- Measurements are estimates in image pixels, not physical wound area in cm².

\- Results depend on image quality and model segmentation accuracy.

\- Changes in lighting, camera angle, distance, and positioning can affect measurements.

\- A change in measured area alone does not establish wound healing.



\## Medical Disclaimer



This project is an educational prototype and is not a medical diagnostic device. It does not replace assessment or advice from a qualified healthcare professional.



