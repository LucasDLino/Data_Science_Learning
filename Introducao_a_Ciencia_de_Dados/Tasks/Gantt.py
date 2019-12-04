from Introducao_a_Ciencia_de_Dados.Tasks.Simulation import Simulation
import pandas as pd
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from random import randrange

from pathlib import Path

class Gantt(object):

    path = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados\Chuvas")

    def __init__(self, file_name):

        self.time_series = pd.Series()
        self.stations = []

        self.file_name = self.path.joinpath(file_name)

        self.all_names = []

        self.gantt_df = pd.DataFrame()

    def read_file(self):
        file = open(str(self.file_name), 'r').read().splitlines()

        position = file.index('#STATIONS')

        n = int(file[position+1])

        for i in range(position+2,position+2+n):
            self.all_names.append(str(file[i]))


    def load_stations(self):
        self.stations.append(self.time_series)

        for i in range(0, len(self.all_names)):
            sim = Simulation(self.all_names[i])
            sim.start()
            sim.running()
            self.stations.append(sim.out.time_series)

    def process_df(self):
        for i in range(0, len(self.stations)):
            series = self.stations[i].dropna().index.to_series()

            start = series[series.diff(1) != pd.Timedelta("1d")].reset_index(drop=True)
            finish = series[series.diff(-1) != -(pd.Timedelta("1d"))].reset_index(drop=True)

            task = pd.Series(index=start).rename(self.stations[i].name)
            task[:] = str(self.stations[i].name)

            self.gantt_df = self.gantt_df.append(pd.DataFrame({"Task": task.values, "Start": start.values, "Finish": finish.values, "Resource": task.values},
                                              columns=["Task", "Start", "Finish", "Resource"]))

        self.gantt_df = self.gantt_df.reset_index(drop=True)

        #self.gantt_df.to_csv(self.path.joinpath('data.csv'), index=False, encoding='utf-8')


    def print_chart(self):
        colors = dict()
        self.all_names.append(self.time_series.name)
        for i in range(0,len(self.all_names)):
            color = (randrange(256),randrange(256),randrange(256))
            color = "rgb"+str(color)
            colors.update({str(self.all_names[i]): color})

        '''data = self.pd.read_csv(self.path.joinpath("data.csv"), sep=",")
        data['Start'] = self.pd.to_datetime(data['Start'])
        data['Finish'] = self.pd.to_datetime(data['Finish'])'''

        data = []

        for row in self.gantt_df.itertuples():
            data.append(dict(Task=str(row[1]), Start=row[2].strftime('%Y-%m-%d'), Finish=row[3].strftime('%Y-%m-%d'),
                             Resource=str(row[4])))

        fig = ff.create_gantt(data, colors=colors, index_col="Resource", show_colorbar=True, group_tasks=True)

        #fig = self.ff.create_gantt(self.gantt_df, colors= colors, index_col="IndexCol", show_colorbar=True, group_tasks=True)

#        fig['layout'].update(autosize=True, margin=dict(l=150))
        #py.iplot(fig, filename='gantt-group-tasks-together', world_readable=True)

        plot(fig)
