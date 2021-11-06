from Manager.DBManager import *


class DataManager:
    def __init__(self, param):
        self.param = param
        self.data = dict(stock=pd.DataFrame(), index=pd.DataFrame())
        self.DBM = DBManager(DB_INFO)

    @L2
    def load_data(self):
        ### 1. Load raw data
        for id, table in zip(['stock', 'index'], self.DBM.get_tables(self.param['universe'])):
            cache_path = join(PATH.INPUT, f"{id}_{self.DBM.get_index_name(self.param['universe'])}.ftr")
            if not exists(cache_path):
                query = "select * from %s"
                self.DBM.read(query % table).to_feather(cache_path)
            self.data[id] = pd.read_feather(cache_path)

        ### 2. Select columns
        for id, df in self.data.items():
            cols = ['date', 'close', 'cap', 'jongmok_code'] if id == 'stock' else ['date', 'close']
            self.data[id] = df[cols]

        ### 3. Select dates
        for id, df in self.data.items():
            df.set_index('date', inplace=True)
            df.index = pd.to_datetime(df.index)
            df.sort_index(inplace=True)
            self.data[id] = df.loc[self.param['start_date']:self.param['end_date']]
