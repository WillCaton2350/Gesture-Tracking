import cv2
import mediapipe
from datetime import datetime

while True:
    previous_timestamp = datetime.now()
    iterate_index = 1
    counter = 0
    break

class handDectector:
    def __init__(self,mode=False,max_hands = 2, detection_confidence = 0.5,tracking_confidence = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mp_hands = mediapipe.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mediapipe.solutions.drawing_utils
        
    def find_hands(self,img,draw=True):
        global counter
        img_rgb = cv2.cvtColor(
        img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        for i in range(iterate_index):
            counter +=1
            print(f'{counter,self.results.multi_hand_landmarks}')
            if self.results.multi_hand_landmarks:
                for i in self.results.multi_hand_landmarks:
                    if draw:
                        self.mp_draw.draw_landmarks(img,i,self.mp_hands.HAND_CONNECTIONS)
            return img
    def find_position(self,img, hand_num=0, draw=True):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            hand_object = self.results.multi_hand_landmarks[hand_num]
            for id, landmark in enumerate(hand_object.landmark):
                # we are mapping the iteration (hand_object) in 
                # the results to the landmark iteration in the nested for loop
                print(id,landmark)
                height, width, _ = img.shape
                channels_x, channels_y = int(landmark.x*width),int(landmark.y*height)
                print(f'{str(id)}:\nLandmark point - axis coordinates: {id} \n'+ str(landmark) + 'Object Pixels : X= ' + str(channels_x) + ' : Y= ' + str(channels_y))
                landmark_list.append([id,channels_x,channels_y])
                # This shows you the x,y and z axis for each point between the landmarks
                if id == 8:
                    cv2.circle(img,(channels_x,channels_y),15,(255,0,255),cv2.FILLED)
            return landmark_list
def main():
    cap = cv2.VideoCapture(0)
    detector = handDectector()
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
if __name__ == "__main__":
    main()
