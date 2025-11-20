class FileIOModule:
    def __init__(self, file_path="keyboard_output.txt"):
        self.file_path = file_path

    def load_text(self):
        try:
            with open(self.file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def save_line(self, line):
        with open(self.file_path, "a") as f:
            f.write(line + "\n")
