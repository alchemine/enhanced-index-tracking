import pandas as pd

from Manager.DBManager import *


class DataManager:
    def __init__(self, param):
        self.param = param
        self.data = dict(stock=pd.DataFrame(), index=pd.DataFrame())
        self.DBM = DBManager(DB_INFO)

    ### Main method ##########################################
    @L2
    def load_data(self, base_price='close'):
        ## 0. Check if PATH.INPUT is exist
        generate_dir(PATH.INPUT)

        ## 1. Load raw data
        self._load_price(base_price)

        ## 2. Preprocess data
        self._preprocess()

        ## 3. Get universe data
        self._load_universe()

        ## 4. Adjust start_date, end_date to nearest business date
        self.param['start_date'] = self.data['date'].iloc[0]
        self.param['end_date']   = self.data['date'].iloc[-1]
    @L3
    def select_universe(self):
        start_date = self.param['cur_date']
        end_date   = self.get_date_from_date(self.param['cur_date'], self.param['train_days'])
        end_date   = self.data['universe'].query(f"cdate < '{end_date}'")['cdate'].values[-1]

        ## 1. Remove Nan
        caps = self.data['cap'].loc[start_date:end_date].dropna(axis='columns', how='any')

        ## 2. Select assets which are in 'cap' and 'universe'
        assets_cap = list(caps.columns)
        assets_unv = self.data['universe'].query(f"cdate == '{end_date}'").sort_values('cap', ascending=False)['jongmok_code'].tolist()
        assets     = [asset for asset in assets_unv if asset in assets_cap]
        print(assets)

        exit()
    ##########################################################

    ### Utility method #######################################
    @L3
    def _load_price(self, base_price):
        ## 1. Get raw data
        for id, table in zip(['stock', 'index'], self.get_tables()):
            self.data[id] = self.DBM.load_data(cache_path=join(PATH.INPUT, f"{id}_{self.get_index_name()}.ftr"),
                                               query=f"select * from {table}", sort='date', time_index='date')

        ## 2. Select columns
        for id, df in self.data.items():
            cols = ['date', base_price, 'cap', 'jongmok_code'] if id == 'stock' else ['date', base_price]
            self.data[id] = df[cols].rename(columns={base_price: 'price'})

        ## 3. Select dates
        for id, df in self.data.items():
            df.set_index('date', inplace=True)

            # df.index = pd.to_datetime(df.index)  # TODO: necessary?
            df.sort_index(inplace=True)
            self.data[id] = df.loc[self.param['start_date']:self.param['end_date']]
    @L3
    def _load_universe(self):
        self.data['universe'] = self.DBM.load_data(cache_path=join(PATH.INPUT, f"universe_{self.param['universe']}.ftr"),
                                                   query=f"select * from pf_universe_slave where pf_universe_id = {self.param['universe']}", sort='cdate', time_index='cdate')
        self.data['universe'] = self.data['universe'].query(f"'{self.param['start_date']}' <= cdate <= '{self.param['end_date']}'")[['jongmok_code', 'cdate', 'cap']]
    @L3
    def _preprocess(self):
        ## 1. Impute missing values
        self.data['stock'] = self.data['stock'].interpolate(method='linear', axis='index')
        self.data['index'] = self.data['index'].interpolate(method='linear')
        self.data['cap']   = self.data['stock'].pivot(columns='jongmok_code', values='cap').interpolate(method='linear', axis='index')

        ## 2. Drop NaN
        for id in ['stock', 'index']:  # cap is processed in Engine
            self.data[id].dropna('index', inplace=True)

        ## 3. Select duplicated dates between stock and index data
        dates = self.data['stock'].index.intersection(self.data['index'].index)
        self.data['stock'] = self.data['stock'].loc[dates]
        self.data['index'] = self.data['index'].loc[dates]

        ## 4. Calculate returns, log returns
        for id in ['stock', 'index']:
            self.data[f'{id}_price']      = self.data[id].pivot(columns='jongmok_code', values='price') if id == 'stock' else self.data[id]['price']
            self.data[f'{id}_return']     = self.data[f'{id}_price'].pct_change().fillna(0)
            self.data[f'{id}_log_return'] = self.data[f'{id}_return'].apply(lambda x: np.log(1 + x))
        self.data['code'] = pd.Series(self.data['stock_price'].columns, dtype=str)
        self.data['date'] = pd.Series(self.data['stock_price'].index, dtype=str)

        del self.data['stock'], self.data['index']

    def get_date_from_date(self, date, days):
        return self.data['date'].iloc[self.data['date'].searchsorted(date)+days]
    def get_tables(self):
        return f"vw_stock_daily_{self.get_index_name()}", f"vw_index_daily_{self.get_index_name()}"
    def get_index_name(self):
        return self.DBM.read(f"select name from pf_universe where id = {self.param['universe']}")['name'].values[0]
    ##########################################################

