import pandas as pd

class Data_Processing(object):

    def __init__(self):
        self.dataset = pd.DataFrame()
        self.time_series = pd.Series()
        self.stations = []

    def processing(self):
        self.dataset.index = pd.to_datetime(self.dataset.index, dayfirst=True)
        self.dataset = self.dataset.loc[~self.dataset.index.duplicated(keep='first')]

        self.dataset = self.dataset.sort_index(ascending=True)
        self.dataset = self.dataset.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',', '.'), errors='coerce'))

        self.time_series = pd.Series(index=self.dataset.index)

        last_dates = pd.Series()

        for index, values in self.time_series.iteritems():
            last_dates = last_dates.append(pd.Series(
                index=pd.date_range(start=index, end=index + pd.offsets.MonthEnd(1), freq='D', closed='right')))

        self.time_series = self.time_series.append(last_dates)
        self.time_series = self.time_series.sort_index(ascending=True)

        for index, values in self.time_series.iteritems():
            if index.is_month_start:
                day = index
                for column in self.dataset.columns[12:43]:
                    self.time_series.loc[day] = self.dataset.loc[index, column]
                    day += pd.Timedelta('1d')
                    if day.is_month_start:
                        break


    def process_all(self):
        for i in range(0, len(self.stations)):
            self.dataset = self.stations[i]
            self.processing()
            self.time_series.name = self.stations[i].name
            self.stations[i] = self.time_series
