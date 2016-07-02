import pandas as pd
import os


class StataConverter():

    def __init__(self, pwd):

        self.baseurl = pwd

    def convert_directory_stata_csv(self):

        for file in os.listdir(self.baseurl):
            if file.endswith('.dta'):
                d = pd.read_stata(self.baseurl + file)
                new_file = ''.join(os.path.basename(file), '.csv')
                pd.DataFrame.to_csv(new_file)
                print('wrote file ', new_file)
                del d

        print(' job complete ')


