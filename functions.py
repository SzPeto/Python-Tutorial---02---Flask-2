import datetime
import os.path

class Functions:

    def __init__(self):
        self.is_first_log = True
        self.log_file = self.create_file_dir("Log\\log.txt")
        self.write_log("************************ Initial run **************************************************\n")

    def write_log(self, text):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.is_first_log:
            with open(self.log_file, "a", encoding="utf-8") as log_file:
                log_file.write(f"\n\n{timestamp} - {text}\n")
            self.is_first_log = False
        else:
            with open(self.log_file, "a", encoding="utf-8") as log_file:
                log_file.write(f"{timestamp} - {text}\n")

    def create_file_dir(self, path_and_file):
        try:
            dir_name = os.path.dirname(path_and_file)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
        except Exception as e:
            if os.path.exists("Log\\log.txt"):
                self.write_log(f"def create_file_dir : {e}")
            else:
                print(f"def create_file_dir : {e}")

        return path_and_file