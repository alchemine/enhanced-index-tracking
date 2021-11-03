### util.py ###################################
# Commonly used functions, classes are defined in here
###############################################


from Env.env import *
from Env.config import *


### lambda functions
tprint = lambda dic: print(tabulate({k: [v] for k, v in dic.items()}, headers='keys', tablefmt='psql'))  # print 'dic' with fancy 'psql' form

list_all   = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path))]
list_dirs  = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isdir(join(path, name))]
list_files = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isfile(join(path, name))]


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
