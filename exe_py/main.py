from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QObject
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image, ImageQt
from cvzone import HandTrackingModule
import numpy as np
import math
import cv2
import sys
import os

class WorkerSignals(QObject):
    frame_updated = pyqtSignal(np.ndarray)
    finished = pyqtSignal()

class HandTrackingWorker(QThread):
    def __init__(self):
        super().__init__()
        self.camera_width, self.camera_height = [640, 480]
        self.current_volume = 0
        self.volume_min = 0
        self.volume_max = 100
        self.detector = HandTrackingModule.HandDetector(maxHands=1, detectionCon=0.3)
        self.signals = WorkerSignals()

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, self.camera_width)
        cap.set(4, self.camera_height)

        while not self.isInterruptionRequested():
            success, img = cap.read()
            hands, img = self.detector.findHands(img, draw=False)

            if hands:
                hand = hands[0]
                x, y, width, height = hand["bbox"]
                cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
                length = math.hypot(hand['lmList'][8][0] - hand['lmList'][4][0], hand['lmList'][8][1] - hand['lmList'][4][1])

                if length < 40:
                    cv2.circle(img, (hand['lmList'][8][0], hand['lmList'][8][1]), 10, (0, 255, 0), cv2.FILLED)

                target_volume = np.interp(length, [40, 200], [self.volume_min, self.volume_max])
                step = 58

                if self.current_volume < target_volume:
                    self.current_volume = min(self.current_volume + step, target_volume)
                elif self.current_volume > target_volume:
                    self.current_volume = max(self.current_volume - step, target_volume)

                os.system(f"osascript -e 'set volume output volume {int(self.current_volume)}'")
                print(f'Volume set to {int(self.current_volume)}')

            self.signals.frame_updated.emit(img)

        self.signals.finished.emit()

    def finish(self):
        self.requestInterruption()
        self.wait()

class HandTrackingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Nesis")
        self.setFixedSize(500, 480)

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("background-color: #191919; color: white;")
        self.start_button.clicked.connect(self.start_tracking)

        gradient_style = '''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #fdbb2d, stop:1 #F7971E);
        '''
        self.setStyleSheet(gradient_style)

        image_path =  '/Users/administrator/Desktop/Projects/exe_py/img/willbg.png'
        # Removing the background from the image worked
        pillow_image = Image.open(image_path)
        q_image = ImageQt.ImageQt(pillow_image)
        pixmap = QPixmap.fromImage(q_image)
        
        self.logo = QLabel(self)
        self.logo.setPixmap(pixmap)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.start_button)
        central_layout.addWidget(self.logo) 
        central_layout.addWidget(self.video_label)
        self.setCentralWidget(central_widget)

        self.hand_tracking_worker = HandTrackingWorker()
        self.hand_tracking_worker.signals.finished.connect(self.worker_finished)

    def start_tracking(self):
        self.hand_tracking_worker.start()

    def display_frame(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap)

    def worker_finished(self):
        self.close()

    def closeEvent(self, event):
        self.hand_tracking_worker.finish()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = HandTrackingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
