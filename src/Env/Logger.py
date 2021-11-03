import sys
import os
from os.path import isdir, join
from datetime import datetime
from pytz import timezone


class Logger:
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

    n1 = 1
    n2 = 1
    n3 = 1
    n4 = 1

    def __init__(self, log_dir_path):
        self.log_dir_path = log_dir_path
        self.change_stdout()
    def change_stdout(self):
        sys.stdout = self.LogOut(self.log_dir_path)


def print_fn(level, name, args, fn):
    print("-"*(level-1) + f"> {name}: ", end='')
    if len(args) > 0 and isinstance(args[0], object):
        print(f"{fn.__module__.split('.')[1]}.", end='')
    print(f"{fn.__name__}()")
