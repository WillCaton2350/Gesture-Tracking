from cvzone import HandTrackingModule
from datetime import datetime
import numpy as np
import math
import cv2
import os

camera_width, camera_height = [640, 480]
cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)
volume_min = 0
volume_max = 100
current_volume = volume_min
os.system(f"osascript -e 'set volume output volume {current_volume}'")
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    detector = HandTrackingModule.HandDetector(maxHands=1, detectionCon=0.3)
    while True:
        previous_timestamp = datetime.now()
        success, img = cap.read()
        hands, img = detector.findHands(img, draw=False)
        if hands:
            hand = hands[0]
            x, y, width, height = hand["bbox"]
            cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
            length = math.hypot(hand['lmList'][8][0] - hand['lmList'][4][0], hand['lmList'][8][1] - hand['lmList'][4][1])
            if length < 40:
                cv2.circle(img, (hand['lmList'][8][0], hand['lmList'][8][1]), 10, (0, 255, 0), cv2.FILLED)
            target_volume = np.interp(length, [40, 200], [volume_min, volume_max])
            step = 60
            if current_volume < target_volume:
                current_volume = min(current_volume + step, target_volume)
            elif current_volume > target_volume:
                current_volume = max(current_volume - step, target_volume)
            os.system(f"osascript -e 'set volume output volume {int(current_volume)}'")
            print(f'Volume set to {int(current_volume)}')
        current_timestamp = datetime.now()
        time_difference = current_timestamp - previous_timestamp
        fps = 1 / time_difference.total_seconds()
        previous_timestamp = current_timestamp
        cv2.putText(img, f'FPS: {int(fps)}', (50, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        cv2.waitKey(1)
        if not success:
            print("Error: Failed to read frame from the camera.")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break