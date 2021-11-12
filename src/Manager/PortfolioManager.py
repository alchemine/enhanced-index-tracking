from Manager.DataManager import *

class PortfolioManager:
    def __init__(self, param):
        self.param  = param
        self.dm     = DataManager(param)

        ## Select Engine mode (CPU or GPU)
        if param['GPU']:
            from Engine.GPU.Engine import Engine
        else:
            from Engine.CPU.Engine import Engine
        self.engine = Engine(self.dm, param)

    @L
    def experiment(self):
        ### 1. Load data
        self.dm.load_data()

        self.param['cur_date'] = self.param['start_date']
        while self.param['cur_date'] <= self.param['end_date']:
            ### 2. Train
            # results = self.engine.train()
            # joblib.dump(results, join(PATH.CKPT, 'results.joblib'))
            results = joblib.load(join(PATH.CKPT, "results.joblib"))

            ### 3. Test
            self.engine.test(results)
            break
