from Env.util import *


class DBManager(metaclass=MetaSingleton):
    def __init__(self, db_info):
        self.conn = pymysql.connect(**db_info)
    def __del__(self):
        self.conn.close()
    def read(self, query):
        return pd.read_sql(query, self.conn)
    def load_data(self, cache_path, query, sort_col=None, time_col=None):
        if not exists(cache_path):
            data = self.read(query)
            data = data.sort_values(sort_col, ignore_index=True) if sort_col else data
            if time_col:
                data[time_col] = data[time_col].astype(str)
            data.to_feather(cache_path)
        return pd.read_feather(cache_path)
