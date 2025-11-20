import time

class GestureModule:
    def __init__(self, hand_open_threshold=3.0):
        self.hand_open_start_time = None
        self.hand_open_threshold = hand_open_threshold

    def is_hand_open(self, landmarks):
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]

        open_count = 0
        try:
            for tip, pip in zip(finger_tips, finger_pips):
                if landmarks[tip].y < landmarks[pip].y:
                    open_count += 1

            if landmarks[4].x < landmarks[3].x:
                open_count += 1
        except:
            return False

        return open_count >= 4

    def handle_clear_gesture(self, landmarks, current_line):
        if self.is_hand_open(landmarks):
            if self.hand_open_start_time is None:
                self.hand_open_start_time = time.time()
            elif time.time() - self.hand_open_start_time >= self.hand_open_threshold:
                self.hand_open_start_time = None
                return ""  # clear
        else:
            self.hand_open_start_time = None

        return current_line
