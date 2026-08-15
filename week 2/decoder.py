import av
import cv2
import time
import os

# Create folder if it doesn't exist
os.makedirs("frames", exist_ok=True)

# Open video
container = av.open("rtsp://192.168.1.8:1945/")

frame_count = 0
start_time = time.time()

for frame in container.decode(video=0):

    frame_count += 1

    img = frame.to_ndarray(format="bgr24")

    # Save each frame
    cv2.imwrite(f"frames/frame_{frame_count}.jpg", img)

    # Display video
    cv2.imshow("Decoded Video", img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

end_time = time.time()

print("\n----- Performance -----")
print("Total Frames :", frame_count)
print("Time Taken :", round(end_time-start_time,2),"seconds")
print("FPS :", round(frame_count/(end_time-start_time),2))

cv2.destroyAllWindows()
