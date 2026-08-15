import cv2

from stream import open_stream, read_frame

try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover - import is optional in starter setup
    YOLO = None


def load_model(model_path="models/yolov8n.pt"):
    if YOLO is None:
        raise RuntimeError("ultralytics is not installed. Install requirements first.")
    return YOLO(model_path)


def draw_detections(frame, detections):
    output = frame.copy()
    for detection in detections:
        x1, y1, x2, y2 = detection["bbox"]
        label = detection["label"]
        confidence = detection["confidence"]

        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
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


def run_detection(model_path="models/yolov8n.pt", source=0):
    model = load_model(model_path)
    cap = open_stream(source)

    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                break

            results = model(frame, stream=False, conf=0.25)
            detections = []
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    label = model.names[int(box.cls[0])]
                    confidence = float(box.conf[0])
                    detections.append(
                        {
                            "bbox": (x1, y1, x2, y2),
                            "label": label,
                            "confidence": confidence,
                        }
                    )

            display_frame = draw_detections(frame, detections)
            cv2.imshow("VisionEdge Detection", display_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run_detection()
