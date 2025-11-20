import time

class HoverSelectionModule:
    def __init__(self, hover_threshold=0.5):
        self.hover_threshold = hover_threshold
        self.current_hover_key = None
        self.hover_start_time = None
        self.last_selected_key = None
        self.last_selected_time = 0

    def update_hover(self, key_info, core_state):
        if key_info:
            i, j, key = key_info

            if self.current_hover_key != (i, j):
                self.current_hover_key = (i, j)
                self.hover_start_time = time.time()
            else:
                if time.time() - self.hover_start_time >= self.hover_threshold:
                    if self.last_selected_key != (i, j) or time.time() - self.last_selected_time > 1.0:
                        self._apply_key_action(key, core_state)

                        self.last_selected_key = (i, j)
                        self.last_selected_time = time.time()

                        self.hover_start_time = time.time()

        else:
            self.current_hover_key = None
            self.hover_start_time = None

    def _apply_key_action(self, key, core_state):
        if key == "SPACE":
            core_state['current_line'] += " "

        elif key == "DEL":
            core_state['current_line'] = core_state['current_line'][:-1]

        elif key == "ENTER":
            core_state['save_text_func']()

        else:
            char_to_add = key

            if len(key) == 1 and key.isalpha() and core_state['keyboard_module'].mode == "alpha":
                if core_state['buttons_module'].caps_lock:
                    char_to_add = key.upper()
                else:
                    char_to_add = key.lower()

            core_state['current_line'] += char_to_add
