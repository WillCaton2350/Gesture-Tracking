from datetime import datetime
import pyautogui as pg
import numpy as np
import cv2
import htm

width_camera = 640
height_camera = 300
width_screen = 1440
height_screen = 900
frame_reduction_x = 100
frame_reduction_y = 80
cap = cv2.VideoCapture(0)
cap.set(3,width_camera)
cap.set(4,height_camera)
previous_timestamp = datetime.now()
detector = htm.handDectector(max_hands=1)
while True:
    success,img = cap.read()
    img = detector.find_hands(img)
    landmark_list, bbox = detector.find_position(img)
    if len(landmark_list)!=0:
        x1,y1 = landmark_list[8][1:]
        x2,y2 = landmark_list[12][1:]
        fingers = detector.fingers_up()
        cv2.rectangle(img,(frame_reduction_x,frame_reduction_y),
        (width_camera - frame_reduction_x,height_camera-frame_reduction_y),
        (255,0,255),2)
        print(fingers) 
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frame_reduction_x, width_camera - frame_reduction_x), (0, width_screen))
            y3 = np.interp(y1, (frame_reduction_y, height_camera - frame_reduction_y), (0, height_screen))
            pg.moveTo(width_screen-x3,y3,duration=0.05)
        if fingers[1] == 1 and fingers[2] == 1:
            length,img, i = detector.find_distance(8,12,img)
            print(length)
            if length < 40:
                cv2.circle(img,(i[4],i[5]),15,(0,255,0),cv2.FILLED)
                pg.click()
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
        break 