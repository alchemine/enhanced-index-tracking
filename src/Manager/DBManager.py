from Env.util import *


class DBManager(metaclass=MetaSingleton):
    def __init__(self, db_info):
        self.conn = pymysql.connect(**db_info)
    def __del__(self):
        self.conn.close()
    def read(self, query):
        return pd.read_sql(query, self.conn)
    def load_data(self, cache_path, query, sort=None, time_index=None):
        if not exists(cache_path):
            self.read(query).to_feather(cache_path)
        data = pd.read_feather(cache_path)
        data = data.sort_values(sort, ignore_index=True) if sort else data
        if time_index:
            data[time_index] = data[time_index].astype(str)
        return data
