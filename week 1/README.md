# VisionEdge

VisionEdge is a beginner-friendly project for detecting objects from a live camera or CCTV stream using YOLO and displaying the results in a web application.

## Architecture

Camera -> OpenCV/PyAV -> YOLO -> TensorRT (optional) -> Backend -> React Frontend -> Browser

## Project Structure

- backend/ - Python streaming and detection scripts
- frontend/ - React app for the UI
- models/ - YOLO ONNX/engine files
- videos/ - sample video files
- utils/ - helper scripts

## Getting Started

1. Create a Python virtual environment.
2. Install Python dependencies:
   - pip install -r requirements.txt
3. Install frontend dependencies:
   - cd frontend
   - npm install
4. Run the backend stream viewer:
   - python backend/stream.py
5. Run the detection demo:
   - python backend/detect.py
6. Start the React app:
   - npm run dev

## Next Steps

- Export YOLO weights to ONNX.
- Convert ONNX to TensorRT engine if GPU support is available.
- Connect the backend detection pipeline to the React frontend.
