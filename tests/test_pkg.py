import pytest
from pkg35_convert_stata_csv.StataConverter import StataConverter
import numpy as np
import pandas as pd



def test_Stata_converter_directory():
    directory = '/media/krishnab/jaimini/work/proj_rsc_antonio6/data/India/'
    t = StataConverter(directory)
    t.convert_directory_stata_csv()


