import time

class ButtonInteractionModule:
    def __init__(self, theme_hold_time=3.0, caps_hold_time=1.0, mode_hold_time=1.0):
        self.theme_hover_start = None
        self.caps_hover_start = None
        self.mode_hover_start = None

        self.dark_mode = True
        self.caps_lock = False

        self.theme_hold_time = theme_hold_time
        self.caps_hold_time = caps_hold_time
        self.mode_hold_time = mode_hold_time

    def check_button_hover(self, x, y, mode_ref):
        # Theme button
        if 10 <= x <= 200 and 100 <= y <= 140:
            if self.theme_hover_start is None:
                self.theme_hover_start = time.time()
            elif time.time() - self.theme_hover_start >= self.theme_hold_time:
                self.dark_mode = not self.dark_mode
                self.theme_hover_start = None
            return True
        else:
            self.theme_hover_start = None

        # Caps button
        if 210 <= x <= 330 and 100 <= y <= 140:
            if self.caps_hover_start is None:
                self.caps_hover_start = time.time()
            elif time.time() - self.caps_hover_start >= self.caps_hold_time:
                self.caps_lock = not self.caps_lock
                self.caps_hover_start = None
            return True
        else:
            self.caps_hover_start = None

        # Mode switch button
        if 340 <= x <= 420 and 100 <= y <= 140:
            if self.mode_hover_start is None:
                self.mode_hover_start = time.time()
            elif time.time() - self.mode_hover_start >= self.mode_hold_time:
                mode_ref['module'].mode = 'symbol' if mode_ref['module'].mode == 'alpha' else 'alpha'
                self.mode_hover_start = None
            return True
        else:
            self.mode_hover_start = None

        return False
