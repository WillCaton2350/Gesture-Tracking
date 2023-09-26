import cv2
from datetime import datetime
import htm_import.hand_tracking_module as htm

cap = cv2.VideoCapture(0)
detector = htm.handDectector()
while True:
    previous_timestamp = datetime.now()
    break
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        detector.find_position(img)
        current_timestamp = datetime.now()
        time_difference = current_timestamp - previous_timestamp
        fps = 1 / time_difference.total_seconds()
        previous_timestamp = current_timestamp
        cv2.putText(img,str(int(fps)),(10,70), 
        cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        if not success:
            print("Error: Failed to read frame from camera.")
            break
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # hash value / id for the q key on the keyboard
            break