import cv2
import mediapipe
from datetime import datetime
cap = cv2.VideoCapture(0)
mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands()
mp_draw = mediapipe.solutions.drawing_utils
while True:
    previous_timestamp = datetime.now()
    iterate_index = 1
    counter = 0
    break
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    while True:
        success, img = cap.read()
        img_rgb = cv2.cvtColor(
        img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        for i in range(iterate_index):
            counter +=1
            print(f'{counter,results.multi_hand_landmarks}')
            if results.multi_hand_landmarks:
                for i in results.multi_hand_landmarks:
                    for id, landmark in enumerate(i.landmark):
                        # we are mapping the iteration (i) in 
                        # the results to the landmark iteration in the nested for loop
                        # print(id,landmark)
                        height,width,channels = img. shape
                        channels_x, channels_y = int(landmark.x*width),int(landmark.y*height)
                        print(f'{str(id)}:\nLandmark point - axis coordinates: {id} \n'+ str(landmark) + 'Object Pixels : X= ' + str(channels_x) + ' : Y= ' + str(channels_y))
                        # This shows you the x,y and z axis for each point between the landmarks
                        #if id == 4:
                        cv2.circle(img,(channels_x,channels_y),15,(255,0,255),cv2.FILLED)
                    mp_draw.draw_landmarks(img,i,mp_hands.HAND_CONNECTIONS)
            current_timestamp = datetime.now()
            time_difference = current_timestamp - previous_timestamp
            fps = 1 / time_difference.total_seconds()
            previous_timestamp = current_timestamp
            cv2.putText(img, str(int(fps)),(10,70), 
            cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        if not success:
            print("Error: Failed to read frame from camera.")
            break
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # hash value / id for the q key on the keyboard
            break