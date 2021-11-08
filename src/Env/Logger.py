import sys
import os
from os.path import isdir, join
from datetime import datetime
from pytz import timezone
from collections import defaultdict


class Logger:
    ## Level log
    level = 1
    level_val = defaultdict(lambda: 1)


    class LogOut:
        def __init__(self, log_dir_path):
            if not isdir(log_dir_path):
                os.makedirs(log_dir_path)
                print(f"[Inform] {log_dir_path} is generated")
            NOW = datetime.now(timezone('Asia/Seoul')).strftime("%y-%m-%d_%H-%M-%S")
            self.terminal = sys.stdout
            self.logger   = open(join(log_dir_path, f"{NOW}.log"), 'w')
        def __del__(self):
            self.logger.close()
        def write(self, msg):
            self.terminal.write(msg)
            self.logger.write(msg)
        def flush(self): pass

    def __init__(self, log_dir_path):
        self.log_dir_path = log_dir_path
        self.change_stdout()
    def change_stdout(self):
        sys.stdout = self.LogOut(self.log_dir_path)
