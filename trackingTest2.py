import cv2
import random
from cv2 import TrackerCSRT_create
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Use file dialog box to select video file
file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])

# Open the video file
video = cv2.VideoCapture(file_path)

drawing = False
roi_points = []
current_box = None

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global drawing, roi_points, current_box

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        roi_points = [(x, y)]

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            current_box = (roi_points[0][0], roi_points[0][1], x - roi_points[0][0], y - roi_points[0][1])

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi_points.append((x, y))
        roi = (roi_points[0][0], roi_points[0][1], roi_points[1][0] - roi_points[0][0], roi_points[1][1] - roi_points[0][1])
        
        # Check if the ROI is valid
        if roi[2] > 0 and roi[3] > 0:
            second_tracker = cv2.TrackerCSRT_create()
            second_tracker.init(frame, roi)
            trackers.append(second_tracker)
            current_box = None

tracker = cv2.TrackerCSRT_create()
trackers = [tracker]
ret, frame = video.read()
frame_height, frame_width, _ = frame.shape
min_roi_size = 10
max_roi_size = 100
x = random.randint(0, frame_width - max_roi_size)
y = random.randint(0, frame_height - max_roi_size)
w = random.randint(min_roi_size, max_roi_size)
h = random.randint(min_roi_size, max_roi_size)
roi = (x, y, w, h)
ret = tracker.init(frame, roi)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_callback)

while True:
    ret, frame = video.read()

    if not ret:
        break

    for idx, tracker in enumerate(trackers):
        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        else:
            cv2.putText(frame, f"Lost {idx+1}", (50, 50 * (idx + 1)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if current_box:
        x, y, w, h = current_box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
