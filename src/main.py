from Interface.Interface import *


parser = ArgumentParser()
parser.add_argument("--cmd", default="experiment")
parser.add_argument("--server_id", default="26037")

parser.add_argument("--start_date", default="2016-01-01")
parser.add_argument("--end_date", default="2021-01-01")
parser.add_argument("--universe", default="13")


if __name__ == '__main__':
    param = parser.parse_args().__dict__
    interface = Interface()
    interface.run(**param)
