import cv2

class InputModule:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.cap = None

    def start(self, device=0):
        self.cap = cv2.VideoCapture(device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)
        return frame

    def stop(self):
        if self.cap:
            self.cap.release()
