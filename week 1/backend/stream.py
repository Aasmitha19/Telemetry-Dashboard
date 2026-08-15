import cv2


def open_stream(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open stream source: {source}")
    return cap


def read_frame(cap):
    ok, frame = cap.read()
    if not ok:
        return None
    return frame


def stream_loop(source=0, window_name="VisionEdge Stream"):
    cap = open_stream(source)
    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                break

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    stream_loop()
