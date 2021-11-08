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
        print(f"[Elapsed time] {self.name}: {elapsed_time:.2f}s ({elapsed_time/60:.2f}m)")
        return False
def L1(fn):
    @wraps(fn)
    def log(*args, **kwargs):
        name = f"L{Logger.n1}"
        with Timer(name):
            print_fn(1, name, args, fn)
            rst = fn(*args, **kwargs)
            Logger.n1 += 1
        print()
        return rst
    return log
def L2(fn):
    @wraps(fn)
    def log(*args, **kwargs):
        name = f"L{Logger.n1}.{Logger.n2}"
        with Timer(name):
            print_fn(2, name, args, fn)
            rst = fn(*args, **kwargs)
            Logger.n2 += 1
        print()
        return rst
    return log
def L3(fn):
    @wraps(fn)
    def log(*args, **kwargs):
        name = f"L{Logger.n1}.{Logger.n2}.{Logger.n3}"
        with Timer(name):
            print_fn(3, name, args, fn)
            rst = fn(*args, **kwargs)
            Logger.n3 += 1
        return rst
    return log
def L4(fn):
    @wraps(fn)
    def log(*args, **kwargs):
        name = f"L{Logger.n1}.{Logger.n2}.{Logger.n3}.{Logger.n4}"
        with Timer(name):
            print_fn(4, name, args, fn)
            rst = fn(*args, **kwargs)
            Logger.n4 += 1
        return rst
    return log


### Singleton superclass
class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
