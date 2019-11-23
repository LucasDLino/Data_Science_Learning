class Input(object):
    import pandas as pd

    def __init__(self,file_name):
        self.file_name = file_name
        self.dataset = self.pd.DataFrame()
    def import_data(self):
        self.dataset = self.pd.read_csv(self.file_name, skiprows=12, sep = ';', index_col=False).set_index('Data', drop=True)
