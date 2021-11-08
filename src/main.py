from Interface.Interface import *


parser = ArgumentParser()

## Server parameter
parser.add_argument("--cmd", default="experiment")
parser.add_argument("--server_id", default="26037")

## Data parameter
parser.add_argument("--start_date", default="2016-01-01")
parser.add_argument("--end_date", default="2021-01-01")
parser.add_argument("--universe", default=13, type=int)
parser.add_argument("--train_days", default=120, type=int)
parser.add_argument("--test_days", default=60, type=int)

## CPU parameter
parser.add_argument("--GPU", default=False, type=str2bool)
parser.add_argument("--K", default=20, type=int)
parser.add_argument("--max_iter_GA", default=50, type=int)
parser.add_argument("--n_pop_GA", default=2**20, type=int)
parser.add_argument("--seed", default=42, type=int)


if __name__ == '__main__':
    param = parser.parse_args().__dict__
    interface = Interface()
    interface.run(**param)
