import cv2
import numpy as np
import time

class UIRenderer:
    def __init__(self, frame_width=1280, frame_height=720):
        self.frame_width = frame_width
        self.frame_height = frame_height

    def create_gradient_background(self, dark_mode):
        height, width = self.frame_height, self.frame_width
        gradient = np.zeros((height, width, 3), dtype=np.uint8)

        if dark_mode:
            for i in range(height):
                ratio = i / height
                gradient[i, :] = [int(80 * ratio), int(50 * ratio), int(20 * ratio)]
        else:
            for i in range(height):
                ratio = i / height
                gradient[i, :] = [int(203 + (255-203)*ratio),
                                  int(192 + (255-192)*ratio),
                                  255]

        return gradient

    def get_colors(self, dark_mode):
        if dark_mode:
            return {
                'key': (60,60,60), 'key_hover': (100,100,100), 'key_active': (0,150,255),
                'text': (255,255,255), 'button': (80,80,80), 'button_active': (0,200,100)
            }
        else:
            return {
                'key': (255,255,255), 'key_hover': (200,200,200), 'key_active': (100,200,255),
                'text': (0,0,0), 'button': (200,200,200), 'button_active': (100,255,150)
            }

    def draw_keyboard(self, frame, keyboard_module, hover_state, buttons_module):
        import time  # local import to avoid circular issues
        colors = self.get_colors(buttons_module.dark_mode)

        keys = keyboard_module.get_active_keys()
        start_x, start_y = keyboard_module.calculate_keyboard_position()

        for i, row in enumerate(keys):
            row_width = 0
            for key in row:
                row_width += (400 if key == "SPACE" else 200 if key == "ENTER" else keyboard_module.key_width) + keyboard_module.key_margin

            row_start_x = start_x + (800 - row_width)//2
            current_x = row_start_x

            for j, key in enumerate(row):
                key_w = 400 if key == "SPACE" else 200 if key == "ENTER" else keyboard_module.key_width
                x = current_x
                y = start_y + i * (keyboard_module.key_height + keyboard_module.key_margin)

                display_key = key
                if len(key) == 1 and key.isalpha() and keyboard_module.mode == 'alpha':
                    display_key = key.upper() if buttons_module.caps_lock else key.lower()

                key_color = colors['key']
                if hover_state.current_hover_key == (i,j) and hover_state.hover_start_time:
                    progress = min(1.0, (time.time() - hover_state.hover_start_time)/hover_state.hover_threshold)
                    key_color = colors['key_hover'] if progress < 1 else colors['key_active']

                cv2.rectangle(frame, (x,y), (x+key_w, y+keyboard_module.key_height), key_color, -1)
                cv2.rectangle(frame, (x,y), (x+key_w, y+keyboard_module.key_height), colors['text'], 2)

                font_scale = 0.6 if len(display_key)>1 else 0.8
                text_size = cv2.getTextSize(display_key, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                text_x = x + (key_w - text_size[0])//2
                text_y = y + (keyboard_module.key_height + text_size[1])//2
                cv2.putText(frame, display_key, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, colors['text'], 2)

                if hover_state.current_hover_key == (i,j) and hover_state.hover_start_time:
                    progress = min(1.0, (time.time() - hover_state.hover_start_time)/hover_state.hover_threshold)
                    bar_width = int(key_w * progress)
                    cv2.rectangle(frame, (x, y + keyboard_module.key_height - 5),
                                  (x + bar_width, y + keyboard_module.key_height),
                                  colors['key_active'], -1)

                current_x += key_w + keyboard_module.key_margin

        return frame

    def draw_ui(self, frame, core_state, buttons_module, hover_state):
        colors = self.get_colors(buttons_module.dark_mode)
        h, w, _ = frame.shape

        cv2.rectangle(frame, (10,10), (w-10,80), colors['key'], -1)
        cv2.rectangle(frame, (10,10), (w-10,80), colors['text'], 2)

        display_text = core_state['current_line'][-80:] if len(core_state['current_line']) > 80 else core_state['current_line']
        cv2.putText(frame, display_text, (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, colors['text'], 2)

        # Theme Button
        cv2.rectangle(frame, (10,100), (200,140), colors['button'], -1)
        cv2.rectangle(frame, (10,100), (200,140), colors['text'], 2)
        theme_text = "Theme: Dark" if buttons_module.dark_mode else "Theme: Light"
        cv2.putText(frame, theme_text, (20,125), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors['text'], 2)

        if buttons_module.theme_hover_start:
            progress = min(1.0, (time.time() - buttons_module.theme_hover_start)/buttons_module.theme_hold_time)
            cv2.rectangle(frame, (10,135), (10 + int(190*progress),140), colors['key_active'], -1)

        # Caps Button
        caps_color = colors['button_active'] if buttons_module.caps_lock else colors['button']
        cv2.rectangle(frame, (210,100), (330,140), caps_color, -1)
        cv2.rectangle(frame, (210,100), (330,140), colors['text'], 2)
        cv2.putText(frame, "CAPS" if buttons_module.caps_lock else "caps",
                    (225,125), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors['text'], 2)

        if buttons_module.caps_hover_start:
            progress = min(1.0, (time.time() - buttons_module.caps_hover_start)/buttons_module.caps_hold_time)
            cv2.rectangle(frame, (210,135), (210+int(120*progress),140), colors['key_active'], -1)

        # Mode Button
        cv2.rectangle(frame, (340,100), (420,140), colors['button'], -1)
        cv2.rectangle(frame, (340,100), (420,140), colors['text'], 2)

        mode_label = "ABC" if core_state['keyboard_module'].mode == 'alpha' else "123"
        cv2.putText(frame, mode_label, (355,125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors['text'], 2)

        if buttons_module.mode_hover_start:
            progress = min(1.0, (time.time() - buttons_module.mode_hover_start)/buttons_module.mode_hold_time)
            cv2.rectangle(frame, (340,135), (340+int(80*progress),140), colors['key_active'], -1)

        # Clear gesture countdown
        if core_state['gesture_module'].hand_open_start_time:
            elapsed = time.time() - core_state['gesture_module'].hand_open_start_time
            remaining = max(0.0, core_state['gesture_module'].hand_open_threshold - elapsed)
            cv2.putText(frame, f"Clear in: {remaining:.1f}s",
                        (w-250,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        return frame
