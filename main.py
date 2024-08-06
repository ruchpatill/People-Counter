import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import Tracker
import datetime
import sqlite3

# Initialize the YOLO model
model = YOLO('yolov8s.pt')

# Mouse callback function for debugging
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Initialize video capture (can be a webcam or an IP camera)
cap = cv2.VideoCapture(0)  # Change '0' to your IP camera stream URL if needed

# Load class names
with open("coco.txt", "r") as f:
    class_list = f.read().split("\n")

# Initialize variables
count = 0
tracker = Tracker()
cy1 = 194
cy2 = 220

# Function to log person detection data into SQLite database
def log_detection(person_id, detection_time):
    conn = sqlite3.connect('detection_log.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO detection_log (person_id, detection_time)
        VALUES (?, ?)
    ''', (person_id, detection_time))
    conn.commit()
    conn.close()

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % 3 != 0:
        continue
    
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    detections = results[0].boxes.data
    detections_df = pd.DataFrame(detections).astype("float")

    bbox_list = []
    for _, row in detections_df.iterrows():
        x1, y1, x2, y2, _, class_id = row
        if class_list[int(class_id)] == 'person':
            bbox_list.append([int(x1), int(y1), int(x2), int(y2)])
    
    bbox_id = tracker.update(bbox_list)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = (x3 + x4) // 2
        cy = (y3 + y4) // 2
        cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)
        log_detection(id, current_time)  # Log the detection

    cv2.line(frame, (3, cy1), (1018, cy1), (0, 255, 0), 2)
    cv2.line(frame, (5, cy2), (1019, cy2), (0, 255, 255), 2)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()