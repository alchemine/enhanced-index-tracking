from Env.util import *


class DBManager(metaclass=MetaSingleton):
    def __init__(self, db_info):
        self.conn = pymysql.connect(**db_info)
    def __del__(self):
        self.conn.close()
    def read(self, query):
        return pd.read_sql(query, self.conn)


    def get_tables(self, universe):
        return f"vw_stock_daily_{self.get_index_name(universe)}", f"vw_index_daily_{self.get_index_name(universe)}"
    def get_index_name(self, universe):
        return self.read(f"select name from pf_universe where id = {universe}")['name'].values[0]
    def get_dates(self, start_date, end_date, param):
        stock_table, _ = self.get_tables(param['universe'])
        prev_date = self.get_date_from_date(start_date, -2, param)  # TODO: check starting before 2 days
        return self.read(f"select distinct(date) from {stock_table} where date between '{prev_date}' and '{end_date}' order by date")['date']
    def get_date_from_date(self, date, days, param):
        stock_table, _ = self.get_tables(param['universe'])
        padding_date = (pd.to_datetime(date) + pd.Timedelta(days=2*days)).strftime('%Y-%m-%d')
        if days >= 0:
            cond = f"where '{date}' < date and date < '{padding_date}' order by date"
        else:
            cond = f"where '{padding_date}' < date and date < '{date}' order by date desc"
        return self.read(f"select distinct(date) from {stock_table} {cond} limit {abs(days)}")['date'].values[-1]
