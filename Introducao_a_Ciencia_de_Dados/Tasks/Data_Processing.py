class Data_Processing(object):
    #from Introducao_a_Ciencia_de_Dados.Tasks import Input
    import pandas as pd
    #input = Input.Input("")

    def __init__(self):
        self.dataset = self.pd.DataFrame()
        self.time_series = self.pd.Series()

    def processing(self):
        self.dataset.index = self.pd.to_datetime(self.dataset.index, dayfirst=True)
        self.dataset = self.dataset.loc[~self.dataset.index.duplicated(keep='first')]

        self.dataset = self.dataset.sort_index(ascending=True)
        self.dataset = self.dataset.apply(lambda x: self.pd.to_numeric(x.astype(str).str.replace(',', '.'), errors='coerce'))

        self.time_series = self.pd.Series(index=self.dataset.index)
        self.time_series.rename('Precipitação (mm)')

        for index, values in self.time_series.iteritems():
            self.time_series = self.time_series.append(self.pd.Series(
                index=self.pd.date_range(start=index, end=index + self.pd.offsets.MonthEnd(1), freq='D', closed='right')))
            if index.is_month_start:
                day = index
                for column in self.dataset.columns[12:43]:
                    self.time_series.loc[day] = self.dataset.loc[index, column]
                    day += self.pd.Timedelta('1d')
                    if day == index.is_month_end:
                        break
        self.time_series = self.time_series.sort_index(ascending=True)