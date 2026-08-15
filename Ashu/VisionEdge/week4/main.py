import time
from pathlib import Path

import cv2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from ultralytics import YOLO


app = FastAPI(title="VisionEdge Week 4 Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_NAME = "yolov8n.pt"
MODEL_PATH = Path("models") / MODEL_NAME
CONFIDENCE = 0.25
JPEG_QUALITY = [int(cv2.IMWRITE_JPEG_QUALITY), 80]


model = None


def load_yolo_model():
    global model

    if model is not None:
        return model

    model_path = str(MODEL_PATH) if MODEL_PATH.exists() else MODEL_NAME

    model = YOLO(model_path)

    return model


def get_detections(frame):
    yolo_model = load_yolo_model()

    results = yolo_model(
        frame,
        stream=False,
        conf=CONFIDENCE,
    )

    detections = []

    for result in results:
        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            label = yolo_model.names[int(box.cls[0])]
            confidence = float(box.conf[0])

            detections.append(
                {
                    "bbox": [x1, y1, x2, y2],
                    "label": label,
                    "confidence": confidence,
                }
            )

    return detections


def draw_detections(frame, detections):
    output = frame.copy()

    for detection in detections:

        x1, y1, x2, y2 = detection["bbox"]
        label = detection["label"]
        confidence = detection["confidence"]

        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            output,
            f"{label} {confidence:.2f}",
            (x1, max(0, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    return output


def open_video_source(source):

    # Camera index such as 0, 1, 2
    if str(source).isdigit():
        source = int(source)

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise RuntimeError(
            f"Unable to open stream source: {source}"
        )

    return cap


def frame_generator(source):

    cap = open_video_source(source)

    try:

        while True:

            ok, frame = cap.read()

            if not ok:
                break

            detections = get_detections(frame)

            output = draw_detections(
                frame,
                detections,
            )

            success, encoded_image = cv2.imencode(
                ".jpg",
                output,
                JPEG_QUALITY,
            )

            if not success:
                continue

            frame_bytes = encoded_image.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )

            time.sleep(0.03)

    finally:
        cap.release()


@app.get("/")
def root():

    return {
        "backend": "VisionEdge",
        "version": "Week 4",
        "message": "Multiple video stream backend is running",
    }


@app.get("/status")
def status():

    model_available = MODEL_PATH.exists()

    try:
        model_loaded = load_yolo_model() is not None
    except Exception:
        model_loaded = False

    return {
        "backend": "VisionEdge",
        "week": 4,
        "backend_ready": True,
        "model_path": (
            str(MODEL_PATH)
            if model_available
            else MODEL_NAME
        ),
        "model_available": model_available,
        "model_loaded": model_loaded,
    }


@app.get("/video_feed/{stream_id}")
def video_feed(
    stream_id: int,
    source: str = "0",
):

    if stream_id < 1:
        raise HTTPException(
            status_code=400,
            detail="stream_id must be 1 or greater",
        )

    try:

        # Test whether the source can be opened
        cap = open_video_source(source)
        cap.release()

    except RuntimeError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return StreamingResponse(
        frame_generator(source),
        media_type=(
            "multipart/x-mixed-replace; "
            "boundary=frame"
        ),
    )


@app.get("/stream_info")
def stream_info():

    return JSONResponse(
        {
            "week": 4,
            "supported_streams": "multiple",
            "example": [
                "/video_feed/1?source=0",
                "/video_feed/2?source=1",
                "/video_feed/3?source=video.mp4",
            ],
        }
    )


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )