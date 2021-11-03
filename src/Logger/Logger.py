from Env.util import *


class Logger:
    class LogOut:
        def __init__(self, log_dir_path):
            generate_dir(log_dir_path)
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


def L1(fn):
    name = f"L{Logger.n1}"
    @Timer(name)
    @wraps(fn)
    def log(*args, **kwargs):
        print_fn(1, name, args, fn)
        return fn(*args, **kwargs)
    Logger.n1 += 1
    return log

def L2(fn):
    name = f"L{Logger.n1}.{Logger.n2}"
    @Timer(name)
    @wraps(fn)
    def log(*args, **kwargs):
        print_fn(2, name, args, fn)
        return fn(*args, **kwargs)
    Logger.n2 += 1
    return log

def L3(fn):
    name = f"L{Logger.n1}.{Logger.n2}.{Logger.n3}"
    @Timer(name)
    @wraps(fn)
    def log(*args, **kwargs):
        print_fn(3, name, args, fn)
        return fn(*args, **kwargs)
    Logger.n3 += 1
    return log

def L4(fn):
    name = f"L{Logger.n1}.{Logger.n2}.{Logger.n3}.{Logger.n4}"
    @Timer(name)
    @wraps(fn)
    def log(*args, **kwargs):
        print_fn(4, name, args, fn)
        return fn(*args, **kwargs)
    Logger.n4 += 1
    return log
