class Output(object):
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    import matplotlib.dates as mdates
    import plotly.figure_factory as ff
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    import plotly.io as pio

    sns.set(rc={'figure.figsize': (11, 9)})

    def __init__(self):
        self.time_series = self.pd.Series()

    def print_years(self):
        fig, axes = self.plt.subplots(3)
        self.plt.subplots_adjust(hspace=0.3)

        axes[2].set_xlabel('Datas')

        for ax in axes:
            ax.set_ylabel('Precipitação (mm)')

        axes[0].plot(self.time_series, linewidth=0.4, color='orange')
        axes[1].plot(self.time_series['1977':'2017'], linewidth=0.4, color='green')
        axes[2].plot(self.time_series['2017'], linewidth=1.2, color='purple')

        axes[2].xaxis.set_major_locator(self.mdates.MonthLocator(bymonthday=1))
        axes[2].xaxis.set_major_formatter(self.mdates.DateFormatter('%b %d'))
        axes[1].xaxis.set_major_locator(self.mdates.YearLocator(base=3))

        axes[0].set_title('Total time series')
        axes[1].set_title('Years: 1977 - 2017')
        axes[2].set_title('Year: 2017')

        fig.show()

    def print_months(self):
        fig, axes = self.plt.subplots(2)
        self.plt.subplots_adjust(hspace=0.3)

        axes[1].set_xlabel('Datas')

        for ax in axes:
            ax.set_ylabel('Precipitação (mm)')

        axes[0].plot(self.time_series['2018-1':'2018-6'], linewidth=1.5, color='green')
        axes[1].plot(self.time_series['2018-6'], linewidth=1.5, color='purple')

        axes[0].xaxis.set_major_locator(self.mdates.MonthLocator(bymonthday=1))
        axes[0].xaxis.set_major_formatter(self.mdates.DateFormatter('%b %d'))
        axes[1].xaxis.set_major_locator(self.mdates.DayLocator(interval=5))
        axes[1].xaxis.set_major_formatter(self.mdates.DateFormatter('%b %d'))

        axes[0].set_title('Time: 2018-1 to 2018-6')
        axes[1].set_title('Month: 2018-6')


    def print_seasonality(self):
        fig = self.plt.subplots()

        time_series_df = self.pd.DataFrame({"Precipitação (mm)": self.time_series.values}, index=self.time_series.index)
        time_series_df["Year"] = self.time_series.index.year
        time_series_df["Month"] = self.time_series.index.month
        time_series_df["Weekday Name"] = self.time_series.index.weekday_name

        fig = self.sns.boxplot(data=time_series_df['2010'], x="Weekday Name", y="Precipitação (mm)")


    def print_down_weekly(self):
        start, end = "1947-01", "1947-06"
        time_series_weekly_mean = self.time_series.resample("W").mean()

        fig, ax = self.plt.subplots()
        ax.plot(self.time_series.loc[start:end], marker=".", linestyle="-", linewidth=0.5, label="Daily")
        ax.plot(time_series_weekly_mean.loc[start:end], marker="o", markersize=8, linestyle="-",
                 label="Weekly Mean Resample")
        ax.set_ylabel("Precipitação (mm)")
        ax.legend()

        fig.show()


    def print_down_monthly(self):
        start, end = "2013-12", "2014"
        time_series_monthly_sum = self.time_series.resample("M").sum(min_count=28)

        fig, ax = self.plt.subplots()
        ax.plot(time_series_monthly_sum.loc[start:end], color="black", label="Monthly")
        self.time_series.loc[start:end].plot.area(ax=ax, linewidth=0, label="Daily")
        ax.xaxis.set_major_locator(self.mdates.MonthLocator())
        ax.legend()
        ax.set_ylabel("Monthly Total of Precipitation (mm)")


    def print_down_yearly(self):
        start, end = "2010", "2018"
        time_series_annual_sum = self.time_series.resample("A").sum(min_count=360)
        time_series_annual_sum.index = time_series_annual_sum.index.year
        time_series_annual_sum.index.name = "Year"

        fig = self.plt.subplots()  # Don't need that
        fig = time_series_annual_sum.loc[start:end].plot.bar(color="C0")
        fig.set_ylabel("Total Annual Precipitation (mm)")
        fig.set_title("Annual Precipitation")
        self.plt.xticks(rotation=0)


    def print_down_rolling_7d(self):
        start, end = "1947-01", "1947-06"
        time_series_7d = self.time_series.rolling(7, center=True).mean()
        time_series_weekly_mean = self.time_series.resample("W").mean()

        fig, ax = self.plt.subplots()
        ax.plot(self.time_series.loc[start:end], marker=".", linestyle="-", linewidth=0.5, label="Daily")
        ax.plot(time_series_weekly_mean.loc[start:end], marker="o", markersize=8, linestyle="-",
                 label="Weekly Mean Resample")
        ax.plot(time_series_7d.loc[start:end], marker=".", linestyle="-", label="7 days Rolling Mean")
        ax.set_ylabel("Precipitação (mm)")
        ax.legend()


    def print_down_rolling_365d(self):
        start, end = "1994", "2006"

        time_series_7d = self.time_series.rolling(7, center=True).mean()
        time_series_365d = self.time_series.rolling(window=365, center=True, min_periods=360).mean()

        fig, ax = self.plt.subplots()
        ax.plot(self.time_series.loc[start:end], marker=".", markersize=2, color="0.6", linestyle="None", label="Daily")
        ax.plot(time_series_7d.loc[start:end], linewidth=2, label="7 days Rolling Mean")
        ax.plot(time_series_365d.loc[start:end], color='0.2', linewidth=3, label="Trend (365 days Rolling Mean)")
        ax.xaxis.set_major_locator(self.mdates.YearLocator())
        ax.legend()
        ax.set_xlabel("Year")
        ax.set_ylabel("Precipitation (mm)")
        ax.set_title("Trends in Precipitations")


    def print_gantt_chart(self):
        pass