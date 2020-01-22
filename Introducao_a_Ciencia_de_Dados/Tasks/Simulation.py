from Introducao_a_Ciencia_de_Dados.Tasks import Output, Data_Processing, Input
from pathlib import Path

class Simulation(object):

    path = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados\Chuvas")

    def __init__(self, file_name):
        self.input = Input.Input(self.path.joinpath(file_name))
        self.process = Data_Processing.Data_Processing()
        self.out = Output.Output()
        self.file_name = file_name
        self.count_stations = -1

    def start(self):
        ### OLHAR
        #self.input.import_data()
        self.input.read_file()
        self.input.load_stations()
        self.process.stations = self.input.stations
        self.process.process_all()

    def running(self):
        ### OLHAR
        #self.process.dataset = self.input.dataset
        #self.process.processing()
        #self.process.time_series.name = str(self.file_name)
        #self.out.time_series = self.process.time_series
        #self.count_stations += 1
        self.out.time_series = self.process.stations[self.count_stations]
        self.plot_all()


    def plot_all(self):
        #self.out.print_years()
        #self.out.print_months()
        #self.out.print_seasonality()
        #self.out.print_down_weekly()
        #self.out.print_down_monthly()
        #self.out.print_down_yearly()
        #self.out.print_down_rolling_7d()
        #self.out.print_down_rolling_365d()
        self.out.print_gc(self.process.stations)
        #self.out.print_iterative()

    def new_data(self, file_name):
        self.input.file_name = self.path.joinpath(file_name)
        self.input.import_data()


    #self.out.time_series = self.stations[0]