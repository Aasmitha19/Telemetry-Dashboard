import time
from pathlib import Path

import cv2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from detect import draw_detections, load_model
from stream import open_stream, read_frame

app = FastAPI(title="VisionEdge Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_NAME = "yolov8n.pt"
MODEL_PATH = Path("models") / MODEL_NAME
CAM_SOURCE = 0
CONFIDENCE = 0.25
JPEG_QUALITY = [int(cv2.IMWRITE_JPEG_QUALITY), 80]

model = None
latest_detections = []


def load_yolo_model():
    global model
    if model is not None:
        return model

    model_path = str(MODEL_PATH) if MODEL_PATH.exists() else MODEL_NAME
    try:
        model = load_model(model_path)
    except RuntimeError:
        model = None

    return model


def get_detections(frame):
    model = load_yolo_model()
    if model is None:
        return []

    results = model(frame, stream=False, conf=CONFIDENCE)
    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            label = model.names[int(box.cls[0])]
            confidence = float(box.conf[0])
            detections.append(
                {
                    "bbox": [x1, y1, x2, y2],
                    "label": label,
                    "confidence": confidence,
                }
            )

    return detections


def frame_generator():
    global latest_detections
    cap = open_stream(CAM_SOURCE)

    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                break

            latest_detections = get_detections(frame)
            output = draw_detections(frame, latest_detections) if latest_detections else frame
            success, encoded_image = cv2.imencode(".jpg", output, JPEG_QUALITY)
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


@app.get("/status")
def status():
    model_available = MODEL_PATH.exists()
    model_loaded = load_yolo_model() is not None
    return {
        "backend": "VisionEdge",
        "backend_ready": True,
        "camera_source": CAM_SOURCE,
        "model_path": str(MODEL_PATH) if model_available else MODEL_NAME,
        "model_available": model_available,
        "model_loaded": model_loaded,
    }


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.get("/detections")
def detections():
    return JSONResponse(
        {
            "detections": latest_detections,
            "count": len(latest_detections),
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, log_level="info")
