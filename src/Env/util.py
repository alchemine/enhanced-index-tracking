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


### DB connection
def read_from_db(query, db_info):
    """Get data from db with db_info and query using pymysql module"""
    conn = pymysql.connect(**db_info)
    data = pd.read_sql(query, conn)
    conn.close()
    return data.astype(str)


### Dates
get_tables = lambda universe: (f"vw_stock_daily_{get_index_name(universe)}", f"vw_index_daily_{get_index_name(universe)}")
get_index_name = lambda universe: read_from_db(f"select name from pf_universe where id = {universe}", DB_INFO)['name'].values[0]
def get_date_from_date(date, days, param):
    stock_table, _ = get_tables(param['universe'])
    padding_date = (pd.to_datetime(date) + pd.Timedelta(days=2*days)).strftime('%Y-%m-%d')
    if days >= 0:
        cond = f"where '{date}' < date and date < '{padding_date}' order by date"
    else:
        cond = f"where '{padding_date}' < date and date < '{date}' order by date desc"
    return read_from_db(f"select distinct(date) from {stock_table} {cond} limit {abs(days)}", DB_INFO)['date'].values[-1]
def get_dates(start_date, end_date, param):
    stock_table, _ = get_tables(param['universe'])
    prev_date = get_date_from_date(start_date, -2, param)  # TODO: check starting before 2 days
    return read_from_db(f"select distinct(date) from {stock_table} where date between '{prev_date}' and '{end_date}' order by date", DB_INFO)['date']
