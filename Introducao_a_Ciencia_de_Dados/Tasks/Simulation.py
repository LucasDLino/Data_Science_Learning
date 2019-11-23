class Simulation(object):
    from Introducao_a_Ciencia_de_Dados.Tasks import Output, Data_Processing, Input
    from pathlib import Path
    path = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados\Chuvas")

    def __init__(self):
        self.input = self.Input.Input(self.path.joinpath("chuvas_C_00937023.csv"))
        self.process = self.Data_Processing.Data_Processing()
        self.out = self.Output.Output()

    def start(self):
        self.input.import_data()

    def running(self):
        self.process.dataset = self.input.dataset
        self.process.processing()
        self.out.time_series = self.process.time_series

    def end(self):
        self.out.print_years()
        self.out.print_months()
        self.out.print_seasonality()
        self.out.print_down_weekly()
        self.out.print_down_monthly()
        self.out.print_down_yearly()
        self.out.print_down_rolling_7d()
        self.out.print_down_rolling_365d()
        self.out.print_gantt_chart()

    def new_data(self, file_name):
        self.input.file_name = self.path.joinpath(file_name)
        self.input.import_data()