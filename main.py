import cv2

from input_module import InputModule
from hand_detection import HandDetectionModule
from finger_tracking import FingerTrackingModule
from gestures import GestureModule
from keyboard_mapping import KeyboardMappingModule
from buttons import ButtonInteractionModule
from hover_selection import HoverSelectionModule
from ui_renderer import UIRenderer
from file_io import FileIOModule

def main():
    input_mod = InputModule()
    hand_mod = HandDetectionModule()
    finger_mod = FingerTrackingModule()
    gesture_mod = GestureModule()
    keyboard_mod = KeyboardMappingModule()
    buttons_mod = ButtonInteractionModule()
    hover_mod = HoverSelectionModule()
    ui = UIRenderer()
    fileio = FileIOModule()

    core_state = {
        "current_line": "",
        "keyboard_module": keyboard_mod,
        "buttons_module": buttons_mod,
        "gesture_module": gesture_mod,
    }

    def save_and_clear():
        line = core_state["current_line"]
        if line.strip():  # optional: avoid saving empty lines
            fileio.save_line(line)
        core_state["current_line"] = ""  # clear box immediately

    core_state["save_text_func"] = save_and_clear

    input_mod.start()

    while True:
        frame = input_mod.read()
        if frame is None:
            break

        gradient = ui.create_gradient_background(buttons_mod.dark_mode)
        frame = cv2.addWeighted(gradient, 0.3, frame, 0.7, 0)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hand_mod.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_mod.draw(frame, hand_landmarks)

                x, y = finger_mod.extract_index_tip(hand_landmarks.landmark, frame.shape)

                core_state["current_line"] = gesture_mod.handle_clear_gesture(
                    hand_landmarks.landmark,
                    core_state["current_line"]
                )

                if buttons_mod.check_button_hover(x, y, {"module": keyboard_mod}):
                    pass
                else:
                    key_info = keyboard_mod.get_key_at_position(x, y)
                    hover_mod.update_hover(key_info, core_state)

                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

        else:
            buttons_mod.theme_hover_start = None
            buttons_mod.caps_hover_start = None
            buttons_mod.mode_hover_start = None

        frame = ui.draw_keyboard(frame, keyboard_mod, hover_mod, buttons_mod)
        frame = ui.draw_ui(frame, core_state, buttons_mod, hover_mod)

        cv2.imshow("Virtual Keyboard", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    input_mod.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
