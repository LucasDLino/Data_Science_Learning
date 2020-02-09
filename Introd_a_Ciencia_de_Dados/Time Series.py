#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.io as pio
from pathlib import Path


####################### Importing Data #############################
path = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados\Chuvas")

dataset = pd.read_csv(path.joinpath('chuvas_C_00937023.csv'), skiprows=12, sep = ';', index_col=False).set_index('Data', drop=True)

######## Zipped File - Piranhas ########
#dataset = pd.read_csv(path.joinpath('chuvas_C_00937023.zip'), skiprows=12, sep = ';', index_col=False, compression='zip').set_index('Data', drop=True)

####### Zipped File - Piranhas - PILAR (MANGUABA) ############
#dataset = pd.read_csv(path.joinpath('chuvas_C_00935014.zip', skiprows=12, sep = ';', index_col=False, compression='zip').set_index('Data', drop=True)

####### Zipped File - Fazenda Boa Fortuna ##########
#dataset = pd.read_csv(path.joinpath('chuvas_C_00935056.zip', skiprows=12, sep = ';', index_col=False, compression='zip').set_index('Data', drop=True)


################### Manupulating the data ########################
dataset.index = pd.to_datetime(dataset.index, dayfirst=True)
dataset = dataset.loc[~dataset.index.duplicated(keep='first')]

dataset = dataset.sort_index(ascending=True)
dataset = dataset.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',','.'), errors='coerce'))

time_series = pd.Series(index=dataset.index)
time_series = (time_series.rename('Precipitação (mm)'))


for index,values in time_series.iteritems():
    time_series = time_series.append(pd.Series(index=pd.date_range(start=index, end=index + pd.offsets.MonthEnd(1), freq='D', closed='right')))
    if index.is_month_start:
        day = index
        for column in dataset.columns[12:43]:
            time_series.loc[day] = dataset.loc[index,column]
            day += pd.Timedelta('1d')
            if day == index.is_month_end:
                break
time_series = time_series.sort_index(ascending=True)

################## Visualization of the data #########################
sns.set(rc={'figure.figsize':(11,9)})

####################### Total and 30 years ##########################
fig, axes = plt.subplots(3)
plt.subplots_adjust(hspace=0.3)

axes[2].set_xlabel('Datas')

for ax in axes:
    ax.set_ylabel('Precipitação (mm)')

axes[0].plot(time_series, linewidth=0.4, color='orange')
axes[1].plot(time_series['1977':'2017'], linewidth=0.4, color='green')
axes[2].plot(time_series['2017'], linewidth=1.2, color='purple')

axes[2].xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
axes[1].xaxis.set_major_locator(mdates.YearLocator(base=3))

axes[0].set_title('Total time series')
axes[1].set_title('Years: 1977 - 2017')
axes[2].set_title('Year: 2017')

################## Six Months and One Month ######################
fig2, axes2 = plt.subplots(2)
plt.subplots_adjust(hspace=0.3)

axes2[1].set_xlabel('Datas')

for ax in axes2:
    ax.set_ylabel('Precipitação (mm)')

axes2[0].plot(time_series['2018-1':'2018-6'], linewidth=1.5, color='green')
axes2[1].plot(time_series['2018-6'], linewidth=1.5, color='purple')

axes2[0].xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
axes2[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
axes2[1].xaxis.set_major_locator(mdates.DayLocator(interval=5))
axes2[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

axes2[0].set_title('Time: 2018-1 to 2018-6')
axes2[1].set_title('Month: 2018-6')

"""
######################  Tries  #######################

#time_series = time_series.reindex(pd.date_range(start=time_series.index.min().date(), end=time_series.index.max().date() + pd.offsets.MonthEnd(1), freq='D'))

        #time_series.loc[index] = dataset.loc[index,'Chuva01']
        
                for day in time_series.index.to_period('d').unique():
            for column in dataset.columns[12:43]:
                if pd.isna(time_series.loc[day.to_timestamp()]):
                    time_series.loc[day.to_timestamp()] = dataset.loc[index, column]
                    check = True
                    break
                    
        for column in dataset.columns[12:43]:
            for day in time_series.index.to_period('d').unique():
                if pd.isna(time_series.loc[day.to_timestamp()]):
                    time_series.loc[day.to_timestamp()] = dataset.loc[index, column]
                    break                   
"""

################# Seasonality ####################
time_series_df = pd.DataFrame({"Precipitação (mm)": time_series.values}, index=time_series.index)
time_series_df["Year"] = time_series.index.year
time_series_df["Month"] = time_series.index.month
time_series_df["Weekday Name"] = time_series.index.weekday_name

fig3, axes3 = plt.subplots(figsize=(11,10))
sns.boxplot(data=time_series_df['2010'], x="Weekday Name", y="Precipitação (mm)")

############ Resampling to a lower frequency (Downsampling)  #############

################ Weekly ################
start, end = "1947-01", "1947-06"
time_series_weekly_mean = time_series.resample("W").mean()

fig4, ax1 = plt.subplots()
ax1.plot(time_series.loc[start:end], marker=".", linestyle="-", linewidth=0.5, label="Daily")
ax1.plot(time_series_weekly_mean.loc[start:end], marker="o", markersize=8, linestyle="-", label="Weekly Mean Resample")
ax1.set_ylabel("Precipitação (mm)")
ax1.legend()

################ Monthly ################
start, end = "2013-12", "2014"
time_series_monthly_sum = time_series.resample("M").sum(min_count=28)

fig5, ax2 = plt.subplots()
ax2.plot(time_series_monthly_sum.loc[start:end], color="black", label="Monthly")
time_series.loc[start:end].plot.area(ax=ax2, linewidth=0, label="Daily")
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.legend()
ax2.set_ylabel("Monthly Total of Precipitation (mm)")

############### Yearly ##################
start, end = "2010", "2018"
time_series_annual_sum = time_series.resample("A").sum(min_count=360)
time_series_annual_sum.index = time_series_annual_sum.index.year
time_series_annual_sum.index.name = "Year"

fig6 = plt.subplots() #Don't need that
ax3 = time_series_annual_sum.loc[start:end].plot.bar(color="C0")
ax3.set_ylabel("Total Annual Precipitation (mm)")
ax3.set_title("Annual Precipitation")
plt.xticks(rotation=0)


######################## Rolling Windows - 7 days #######################
start, end = "1947-01", "1947-06"
time_series_7d = time_series.rolling(7, center=True).mean()
time_series_weekly_mean = time_series.resample("W").mean()

fig7, ax4 = plt.subplots()
ax4.plot(time_series.loc[start:end], marker=".", linestyle="-", linewidth=0.5, label="Daily")
ax4.plot(time_series_weekly_mean.loc[start:end], marker="o", markersize=8, linestyle="-", label="Weekly Mean Resample")
ax4.plot(time_series_7d.loc[start:end], marker=".", linestyle="-", label="7 days Rolling Mean")
ax4.set_ylabel("Precipitação (mm)")
ax4.legend()

######################## Rolling Windows - 365 days #######################
start, end = "1994", "2006"
time_series_365d = time_series.rolling(window=365, center=True, min_periods=360).mean()

fig8, ax5 = plt.subplots()
ax5.plot(time_series.loc[start:end], marker=".", markersize=2, color="0.6", linestyle="None", label="Daily")
ax5.plot(time_series_7d.loc[start:end], linewidth=2, label="7 days Rolling Mean")
ax5.plot(time_series_365d.loc[start:end], color='0.2', linewidth=3, label="Trend (365 days Rolling Mean)")
ax5.xaxis.set_major_locator(mdates.YearLocator())
ax5.legend()
ax5.set_xlabel("Year")
ax5.set_ylabel("Precipitation (mm)")
ax5.set_title("Trends in Precipitations")

################ Gantt Chart ###################
"""time_series_df = pd.DataFrame({"Precipitação (mm)": time_series.values}, index=False)
time_series_df["Tempo"] = time_series.index
time_series_df["Year"] = time_series.index.year
time_series_df["Month"] = time_series.index.month
time_series_df["Weekday Name"] = time_series.index.weekday_name"""

### O dataframe deve incluir as colunas "Task", "Start" e "Finish" e outra colunas podem ser incluídas
#Em Task: Nomes dos meses
#Criar coluna de precipitação contendo a soma da precipiação do mês do referido ano em start até o ano em finish
#Passar o dataframe na função create_gantt e assim plotar o diagrama de gantt

path_gantt = Path(r"C:\Users\lucas\PycharmProjects\Data_Science_Learning\Introducao_a_Ciencia_de_Dados")

gantt_chart = pd.read_csv(path_gantt.joinpath("Gantt Chart.csv"), sep =';')
gantt_chart['Start'] = pd.to_datetime(gantt_chart['Start'], dayfirst=True)
gantt_chart['Finish'] = pd.to_datetime(gantt_chart['Finish'], dayfirst=True)

colors = {'Not Started': 'rgb(220, 0, 0)',
          'Incomplete': (1, 0.9, 0.16),
          'Complete': 'rgb(0, 255, 100)'}

fig = ff.create_gantt(gantt_chart, colors= colors, index_col='Resource', show_colorbar=True, group_tasks=True)

plot(fig)

'''    Available renderers:
        ['pdf', 'plotly_mimetype', 'json', 'colab', 'jupyterlab',
         'svg', 'vscode', 'iframe', 'nteract', 'chrome', 'databricks',
         'iframe_connected', 'azure', 'cocalc', 'notebook', 'png',
         'sphinx_gallery', 'jpg', 'jpeg', 'firefox', 'chromium',
         'browser', 'kaggle', 'notebook_connected']'''

#dataset = pd.read_csv('Introd_a_Ciencia_de_Dados/chuvas_C_00937023.csv', skiprows=12, sep = ';', index_col=False).set_index('Data', drop=True)
