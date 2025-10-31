import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2

# --- Funkcja do automatycznego wykrywania działającej kamery ---
def find_working_camera(max_index=5):
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                return i
    return None

class EyeBlinkApp(QWidget):
    def __init__(self):
        super().__init__()

        # --- Ustawienia okna ---
        self.setWindowTitle("Eye Blink Communicator")
        self.setGeometry(100, 100, 800, 600)

        # --- Widżety GUI ---
        self.video_label = QLabel("Camera feed will appear here")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_button = QPushButton("Start Camera")
        self.stop_button = QPushButton("Stop Camera")
        self.status_label = QLabel("Status: Stopped")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # --- Kamera i timer ---
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # --- Połączenia przycisków ---
        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)

    def start_camera(self):
        index = find_working_camera()
        if index is None:
            self.status_label.setText("❌ Nie znaleziono działającej kamery.")
            return

        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.status_label.setText("❌ Kamera nie została znaleziona.")
            return

        self.timer.start(30)
        self.status_label.setText(f"✅ Kamera działa (index {index}).")

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.clear()
        self.status_label.setText("⏹ Kamera zatrzymana.")

    def update_frame(self):
        if self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_img))
        else:
            self.status_label.setText("⚠️ Brak obrazu z kamery.")

    def closeEvent(self, event):
        self.stop_camera()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EyeBlinkApp()
    window.show()
    sys.exit(app.exec())
