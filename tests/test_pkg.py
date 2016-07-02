import pytest
from pkg35_convert_stata_csv.Stata_Converter import
import numpy as np
import pandas as pd



def test_Stata_converter_directory():
    directory = '/media/krishna/jaimini/work/proj_rsc_antonio6/data/India/'
    t = Stata_Converter(directory)
    t.convert_directory_stata_csv()


