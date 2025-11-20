class FingerTrackingModule:
    def __init__(self, smooth_alpha=0.6, max_history=8):
        self.smooth_alpha = smooth_alpha
        self.smooth_x = None
        self.smooth_y = None
        self.pos_history = []
        self.max_history = max_history

    def extract_index_tip(self, landmarks, frame_shape):
        h, w = frame_shape[:2]
        idx = landmarks[8]

        raw_x, raw_y = int(idx.x * w), int(idx.y * h)

        if self.smooth_x is None:
            self.smooth_x, self.smooth_y = raw_x, raw_y

        self.smooth_x = int(self.smooth_alpha * self.smooth_x + (1 - self.smooth_alpha) * raw_x)
        self.smooth_y = int(self.smooth_alpha * self.smooth_y + (1 - self.smooth_alpha) * raw_y)

        x, y = self.smooth_x, self.smooth_y

        self.pos_history.append((x, y))
        if len(self.pos_history) > self.max_history:
            self.pos_history.pop(0)

        return x, y
