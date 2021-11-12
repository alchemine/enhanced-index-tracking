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

## Engine parameter
parser.add_argument("--debug", default=True, type=str2bool)
parser.add_argument("--GPU", default=False, type=str2bool)
parser.add_argument("--K", default=20, type=int)
parser.add_argument("--max_iter_GA", default=5, type=int)
parser.add_argument("--max_iter_EV", default=5, type=int)
parser.add_argument("--n_pop_GA", default=2**14, type=int)
parser.add_argument("--n_pop_EV", default=2**18, type=int)
parser.add_argument("--n_candidate_GA", default=2**10, type=int)
parser.add_argument("--seed", default=42, type=int)
parser.add_argument("--fitness_fn", default='downside_risk')
parser.add_argument("--filter", default='cap')
parser.add_argument("--maximize_fitness", default=False, type=str2bool)
parser.add_argument("--mutation_rate_GA", default=0.1, type=float)
parser.add_argument("--F", default=0.4, type=float)
parser.add_argument("--weight_init_method_GA", default='cap')
parser.add_argument("--weight_init_method_EV", default='weighted')
parser.add_argument("--weight_init_threshold_EV", default=0.1, type=float)
parser.add_argument("--rebalancing_return_threshold", default=-0.05, type=float)



if __name__ == '__main__':
    param = parser.parse_args().__dict__
    interface = Interface()
    interface.run(**param)
