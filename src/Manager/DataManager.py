import pandas as pd

from Manager.DBManager import *


class DataManager:
    def __init__(self, param):
        self.param = param
        self.data = dict(stock=pd.DataFrame(), index=pd.DataFrame())
        self.DBM = DBManager(DB_INFO)

    ### Public method ########################################
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
    @L4
    def select_universe(self):
        ## 1. Set date and index
        start_date = self.param['cur_date']
        end_date   = self._get_date_from_date(self.param['cur_date'], self.param['train_days'] - 1)

        ## 2. Remove Nan
        caps = self.data['cap'].loc[start_date:end_date].dropna(axis='columns', how='any')

        ## 3. Select assets which are in 'cap' and 'universe'
        assets_cap = list(caps.columns)
        end_date_unv = self.data['universe'].query(f"cdate <= '{end_date}'")['cdate'].values[-1]  # nearest date
        assets_unv = self.data['universe'].query(f"cdate == '{end_date_unv}'").sort_values('cap', ascending=False)['jongmok_code'].tolist()
        assets     = [asset for asset in assets_unv if asset in assets_cap]

        ## 4. Result data
        data = {}
        data['date'] = np.array(self.data['stock_price'].index)
        data['asset'] = np.array(assets)  # sorted by cap
        data['cap']   = np.array(caps[assets], dtype=np.float32)
        for key in [f"{data_id}_{type}" for data_id in ['stock', 'index'] for type in ['price', 'return', 'log_return']]:
            data[key] = self.data[key].loc[start_date:end_date]
            data[key] = data[key][assets] if 'stock' in key else data[key]
            data[key] = np.array(data[key], dtype=np.float32)
        return data
    ##########################################################


    ''
    ### Private method #######################################
    @L3
    def _load_price(self, base_price):
        ## 1. Get raw data
        for id, table in zip(['stock', 'index'], self._get_tables()):
            self.data[id] = self.DBM.load_data(cache_path=join(PATH.INPUT, f"{id}_{self._get_index_name()}.ftr"),
                                               query=f"select * from {table}", sort_col='date', time_col='date')

        ## 2. Select columns
        for id, df in self.data.items():
            cols = ['date', base_price, 'cap', 'jongmok_code'] if id == 'stock' else ['date', base_price]
            self.data[id] = df[cols].rename(columns={base_price: 'price'})

        ## 3. Select dates
        for id, df in self.data.items():
            df.set_index('date', inplace=True)
            self.data[id] = df.loc[self.param['start_date']:self.param['end_date']]
    @L3
    def _load_universe(self):
        self.data['universe'] = self.DBM.load_data(cache_path=join(PATH.INPUT, f"universe_{self.param['universe']}.ftr"),
                                                   query=f"select * from pf_universe_slave where pf_universe_id = {self.param['universe']}", sort_col='cdate', time_col='cdate')
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
        self.data['code'] = pd.Series(self.data['stock_price'].columns)
        self.data['date'] = pd.Series(self.data['stock_price'].index)

        del self.data['stock'], self.data['index']
    def _get_date_from_date(self, date, days):
        return self.data['date'].iloc[self.data['date'].searchsorted(date)+days]
    def _get_tables(self):
        return f"vw_stock_daily_{self._get_index_name()}", f"vw_index_daily_{self._get_index_name()}"
    def _get_index_name(self):
        return self.DBM.read(f"select name from pf_universe where id = {self.param['universe']}")['name'].values[0]
    ##########################################################
