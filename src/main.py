from Env.util import *
from Interface.Interface import *


parser = ArgumentParser()
parser.add_argument("--CMD", default="save_data")
parser.add_argument("--SERVER_ID", default="26037", type=int)


if __name__ == '__main__':
    param = parser.parse_args().__dict__
    interface = Interface()
    interface.run(**param)
