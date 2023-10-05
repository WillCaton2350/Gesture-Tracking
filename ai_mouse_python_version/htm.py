from datetime import datetime
import mediapipe
import math 
import cv2

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
        self.tip_ids = [4,8,12,16,20]
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
        self.landmark_list = []
        bbox = []
        x_list = []
        y_list = []
        if self.results.multi_hand_landmarks:
            hand_object = self.results.multi_hand_landmarks[hand_num]
            for id, landmark in enumerate(hand_object.landmark):
                print(id,landmark)
                height, width, _ = img.shape
                channels_x, channels_y = int(landmark.x*width),int(landmark.y*height)
                print(f'{str(id)}:Landmark point - axis coordinates: \n'+ str(landmark) + '\nObject Pixels : X= ' + str(channels_x) + ' : Y= ' + str(channels_y)+"\n")
                x_list.append(channels_x)
                y_list.append(channels_y)
                self.landmark_list.append([id,channels_x,channels_y])
                if draw == True:
                    cv2.circle(img,(channels_x,channels_y),15,(255,0,255),cv2.FILLED)
            x_min = min(x_list)
            x_max = max(x_list)
            y_min = min(y_list)
            y_max = max(y_list)
            bbox = x_min,x_max,y_min,y_max
            if draw == True:
                    cv2.circle(img,(channels_x,channels_y),
                        15,(255,0,255),cv2.FILLED)
        return self.landmark_list, bbox
    def fingers_up(self):
        fingers = []
        if self.landmark_list[self.tip_ids[0]][1] > self.landmark_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if self.landmark_list[self.tip_ids[id]][2] < self.landmark_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    def find_distance(self,p1,p2,img,draw=True,r=15,t=3):
        x1,y1 = self.landmark_list[p1][1:]
        x2,y2 = self.landmark_list[p2][1:]
        channel_x,channel_y = (x1 + x2) // 2,(y1 + y2) // 2
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t)
            cv2.circle(img,(x1,y1),r,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),r,(255,0,255),cv2.FILLED)
            cv2.circle(img,(channel_x,channel_y),r,(0,0,255),cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length,img,[x1,x2,y1,y2,channel_x,channel_y]
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
                break
if __name__ == "__main__":
    main()