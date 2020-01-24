import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from random import randrange

from pathlib import Path

class Gantt(object):

    path = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados\Chuvas")

    def __init__(self, stations):
        self.stations = stations
        self.gantt_df = pd.DataFrame()


    def process_df(self):
        for i in range(0, len(self.stations)):
            series = self.stations[i].dropna().index.to_series()

            start = series[series.diff(1) != pd.Timedelta("1d")].reset_index(drop=True)
            finish = series[series.diff(-1) != -(pd.Timedelta("1d"))].reset_index(drop=True)

            task = pd.Series(index=start) #.rename(self.stations[i].name)

            task.name = self.stations[i].name

            task[:] = str(self.stations[i].name)

            self.gantt_df = self.gantt_df.append(pd.DataFrame({"Task": task.values, "Start": start.values, "Finish": finish.values, "Resource": task.values},
                                              columns=["Task", "Start", "Finish", "Resource"]))

        self.gantt_df = self.gantt_df.reset_index(drop=True)

        #self.gantt_df.to_csv(self.path.joinpath('data.csv'), index=False, encoding='utf-8')


    def print_chart(self):
        colors = dict()
        #self.all_names.append(self.time_series.name)
        for i in range(0,len(self.stations)):
            color = (randrange(256),randrange(256),randrange(256))
            color = "rgb"+str(color)
            colors.update({str(self.stations[i].name): color})

        '''data = self.pd.read_csv(self.path.joinpath("data.csv"), sep=",")
        data['Start'] = self.pd.to_datetime(data['Start'])
        data['Finish'] = self.pd.to_datetime(data['Finish'])'''

        data = []

        for row in self.gantt_df.itertuples():
            data.append(dict(Task=str(row[1]), Start=row[2].strftime('%Y-%m-%d'), Finish=row[3].strftime('%Y-%m-%d'),
                             Resource=str(row[4])))

        fig_gc = ff.create_gantt(data, colors=colors, index_col="Resource", show_colorbar=True, group_tasks=True)

        table = go.Table(
        header=dict(
            values=["Station", "Start Period","End Period"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[self.gantt_df[k].tolist() for k in self.gantt_df.columns[:-1]],
            align = "left")
    )

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,specs=[[{"type": "table"}], [{}]])

        for trace in fig_gc.data:
            fig.add_trace(trace, row=2,col=1)

        fig.add_trace(table, row=1, col=1)

        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Gantt Chart with its Table"
        )
        fig.layout.yaxis.update(fig_gc.layout.yaxis)

        plot(fig)

