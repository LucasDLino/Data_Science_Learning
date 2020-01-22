import pandas as pd
from pathlib import Path

class Input(object):

    path = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados\Chuvas")

    def __init__(self,file_name):
        self.file_name = file_name
        self.dataset = pd.DataFrame()

        ### OLHAR
        self.all_names = []
        self.stations = []

    def import_data(self):
        self.dataset = pd.read_csv(self.file_name, skiprows=12, sep = ';', index_col=False).set_index('Data', drop=True)

    ### OLHAR
    def read_file(self):
        file = open(str(self.file_name), 'r').read().splitlines()

        position = file.index('#STATIONS')

        n = int(file[position+1])

        for i in range(position+2,position+2+n):
            self.all_names.append(str(file[i]))


    def load_stations(self):
        for i in range(0, len(self.all_names)):
            self.file_name = self.path.joinpath(self.all_names[i])
            self.import_data()
            self.dataset.name = self.all_names[i]
            self.stations.append(self.dataset)