### util.py ###################################
# Commonly used functions, classes are defined in here
###############################################


from Env.env import *
from Env.computer import *
from Env.config import *


### lambda functions
tprint = lambda dic: print(tabulate({k: [v] for k, v in dic.items()}, headers='keys', tablefmt='psql'))  # print 'dic' with fancy 'psql' form

list_all   = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path))]
list_dirs  = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isdir(join(path, name))]
list_files = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isfile(join(path, name))]

dt2str = lambda dt: dt.strftime('%Y-%m-%d')
str2dt = lambda s: pd.to_datetime(s).date()


### PATH
class PATH:
    ROOT   = abspath(dirname(os.getcwd()))
    SRC    = join(ROOT, 'src')
    INPUT  = join(ROOT, 'input')
    OUTPUT = join(ROOT, 'output')
    TRAIN  = join(INPUT, 'train')
    TEST   = join(INPUT, 'test')
    CKPT   = join(SRC, 'ckpt')
    RESULT = join(ROOT, 'result')
    LOG    = join(ROOT, 'log')

def generate_dir(path):
    if not isdir(path):
        os.makedirs(path)
        print(f"[Inform] {path} is generated")
def remove_dir(path):
    if isdir(path):
        shutil.rmtree(path)


### Logger decorator
logger = Logger(PATH.LOG)


class Timer(ContextDecorator):
    def __init__(self, name='no_name'):
        self.name = name
    def __enter__(self):
        self.start_time = time()
        return self
    def __exit__(self, *exc):
        elapsed_time = time() - self.start_time
        if elapsed_time > 1:
            print(f" * {self.name} [{elapsed_time:.2f}s]")  # ({elapsed_time/60:.2f}m)
        return False


def print_fn(name, args, fn):
    print(f"-> {name} ", end='')
    if len(args) > 0 and isinstance(args[0], object):
        print(f"{fn.__module__.split('.')[1]}.", end='')
    print(f"{fn.__name__}()")


def L(fn):
    @wraps(fn)
    def log(*args, **kwargs):
        ## Enter
        name = '.'.join([str(Logger.level_val[l]) for l in range(1, Logger.level+1)])
        name = f"{name:<15}"
        print_fn(name, args, fn)
        Logger.level += 1  # dive into

        ## Execute
        with Timer(name):
            rst = fn(*args, **kwargs)

        ## Exit
        Logger.level -= 1  # rise out
        Logger.level_val[Logger.level] += 1
        return rst
    return log


### Singleton superclass
class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
