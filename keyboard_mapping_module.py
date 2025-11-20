class KeyboardMappingModule:
    def __init__(self):
        self.alpha_keys = [
            ['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L'],
            ['Z','X','C','V','B','N','M','DEL'],
            ['SPACE','ENTER']
        ]

        self.symbol_keys = [
            ['1','2','3','4','5','6','7','8','9','0'],
            ['!','@','#','$','%','^','&','*','(',')'],
            ['-','_','+','=','/','\\','|','DEL'],
            ['SPACE','ENTER']
        ]

        self.mode = 'alpha'

        self.key_width = 60
        self.key_height = 60
        self.key_margin = 10
        self.frame_width = 1280
        self.frame_height = 720

    def get_active_keys(self):
        return self.alpha_keys if self.mode == 'alpha' else self.symbol_keys

    def calculate_keyboard_position(self):
        keys = self.get_active_keys()
        max_row_width = 0

        for row in keys:
            row_width = 0
            for key in row:
                if key == "SPACE":
                    row_width += 400 + self.key_margin
                elif key == "ENTER":
                    row_width += 200 + self.key_margin
                else:
                    row_width += self.key_width + self.key_margin
            max_row_width = max(max_row_width, row_width)

        start_x = (self.frame_width - max_row_width) // 2
        start_y = 250
        return start_x, start_y

    def get_key_at_position(self, x, y):
        keys = self.get_active_keys()
        start_x, start_y = self.calculate_keyboard_position()

        for i, row in enumerate(keys):
            row_width = 0
            for key in row:
                if key == "SPACE":
                    row_width += 400 + self.key_margin
                elif key == "ENTER":
                    row_width += 200 + self.key_margin
                else:
                    row_width += self.key_width + self.key_margin

            row_start_x = start_x + (800 - row_width) // 2
            current_x = row_start_x

            for j, key in enumerate(row):
                key_w = 400 if key == "SPACE" else 200 if key == "ENTER" else self.key_width
                key_x = current_x
                key_y = start_y + i * (self.key_height + self.key_margin)

                if key_x <= x <= key_x + key_w and key_y <= y <= key_y + self.key_height:
                    return (i, j, key)

                current_x += key_w + self.key_margin

        return None
