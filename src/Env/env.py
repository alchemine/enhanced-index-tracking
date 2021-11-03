### envs.py ####################################
# Commonly used packages are defined in here
###############################################


### Internal packages
import sys
import os
from argparse import ArgumentParser
from os.path import join, isdir, isfile, exists, basename, dirname, split, abspath
from datetime import datetime, timedelta
from pytz import timezone
import joblib
import json
import re
from itertools import product
from functools import wraps
from time import time, sleep
from collections import defaultdict
from copy import deepcopy as copy
from tqdm import tqdm
import shutil
from dataclasses import dataclass
from contextlib import ContextDecorator



### External packages
import numpy as np
import pandas as pd
from tabulate import tabulate
from numba import njit, cuda
from dask import delayed, compute
from dask.distributed import Client
from switch import Switch
from parse import parse, search


## Plot packages
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import PIL
from PIL import Image


## Matplotlib options
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rc('font', family='DejaVu Sans')
plt.rc('axes', unicode_minus=False)  # Remove warning (Glyps 8722)


### Set options
np.set_printoptions(suppress=True, precision=6, edgeitems=20, linewidth=1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.width', 1000)


### Set signal handler
from Env.SignalHandler import *
SignalHandler.register_signal(signal.SIGINT)
