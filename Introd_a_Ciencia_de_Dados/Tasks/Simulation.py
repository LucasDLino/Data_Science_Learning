from Introd_a_Ciencia_de_Dados.Tasks import Output, Data_Processing, Input, SQL_Task
from pathlib import Path

class Simulation(object):

    path = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados\Chuvas")

    def __init__(self, file_name):
        self.input = Input.Input(self.path.joinpath(file_name))
        self.process = Data_Processing.Data_Processing()
        self.out = Output.Output()
        self.file_name = file_name
        self.count_stations = 0

    def start(self):
        self.input.read_file()
        self.input.load_stations()
        self.process.stations = self.input.stations
        self.process.process_all()

    def running(self):
        self.out.time_series = self.process.stations[self.count_stations]
        #self.plot_all()
        self.sql_run()


    def plot_all(self):
        self.out.print_years()
        #self.out.print_months()
        #self.out.print_seasonality()
        #self.out.print_down_weekly()
        #self.out.print_down_monthly()
        #self.out.print_down_yearly()
        #self.out.print_down_rolling_7d()
        #self.out.print_down_rolling_365d()
        #self.out.print_gc(self.process.stations)
        #self.out.print_iterative()

    def sql_run(self):
        sql_task = SQL_Task.SQL_Class(self.process.stations)
        sql_task.sql_task()