### Using a wrapper to access Alpha Vantage API
'''from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key='ALPHAVANTAGE_API_KEY', output_format='pandas', indexing_type='date')

data2, metadata2 = ts.get_daily(symbol='PETR3.SA', outputsize='full') #Petroleo Brasileiro S.A. - Petrobras (PETR3.SA)

data2['4. close'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()'''

### Using requests to access Alpha Vantage API
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objects as go

API_URL = "https://www.alphavantage.co/query"

print("Exemplos de ações:\nPERT3.SA -> Petroleo Brasileiro S.A. - Petrobras"
      "\nTEND3.SA -> Construtora Tenda S.A."
      "\nLREN3.SA -> Lojas Renner S.A."
      "\nEQTL3.SA -> Equatorial Energia S.A."
      "\nSLCE3.SA -> SLC Agricola S.A.")
#symbol = 'PETR3.SA'
symbol = str(input("Digite o código da ação: "))

data = { "function": "TIME_SERIES_DAILY",
         "symbol": symbol,
         "outputsize" : "full",
         "datatype": "json",
         "apikey": "ALPHAVANTAGE_API_KEY" }

response_json = requests.get(API_URL, params=data).json()
#response_json = response.json() # maybe redundant

while list(response_json.keys())[0] == "Error Message":
    print("O símbolo \"%s\" não corresponde ao símbolo de uma ação." %symbol)
    symbol = str(input("Digite o código da ação novamente: "))
    data["symbol"] = symbol
    response_json = requests.get(API_URL, params=data).json()

### Tratamento do DataFrame dos preços
data = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
data = data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
data = data[[ 'Open', 'High', 'Low', 'Close', 'Volume']] ## Os preços finais já foram ajustados
data.index = pd.to_datetime(data.index)
data = data.sort_index(ascending=True)
data = data.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',', '.'), errors='coerce'))

meta_data = pd.DataFrame.from_dict(response_json['Meta Data'], orient= 'index').sort_index(axis=1)

closed_price = data['Close']

# Calculate the 20 and 100 days moving averages of the closing prices
short_rolling = closed_price.rolling(window=20).mean()
long_rolling = closed_price.rolling(window=100).mean()

# Plot everything by leveraging the very powerful matplotlib package
fig, ax = plt.subplots(figsize=(16,9))

ax.plot(closed_price.index, closed_price, label=symbol)
ax.plot(short_rolling.index, short_rolling, label='20 days rolling')
ax.plot(long_rolling.index, long_rolling, label='100 days rolling')

ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.set_title(symbol)
ax.legend()


#### Ploting Seasonality
sns.set(rc={'figure.figsize': (11, 9)})
plt.subplots()
#data["Year"] = data.index.year
data["Month"] = data.index.month
#data["Weekday Name"] = data.index.weekday_name
sns.boxplot(data=data['2017'], x="Month", y=data["Close"])
plt.title(symbol)


#### Ploting Iterative chart
data["Dates"] = data.index
iterative_figure = go.Figure()

iterative_figure.add_trace(go.Scatter(x=data["Dates"], y=data["Open"], name="Opening Price", line_color='deepskyblue'))
iterative_figure.add_trace(go.Scatter(x=data["Dates"], y=data["High"], name="High Price", line_color='mediumseagreen'))
iterative_figure.add_trace(go.Scatter(x=data["Dates"], y=data["Low"], name="Low Price", line_color='darkorange'))
iterative_figure.add_trace(go.Scatter(x=data["Dates"], y=data["Close"], name="Closing Price", line_color='goldenrod'))
iterative_figure.update_layout(title_text='Prices with Rangeslider',
                  xaxis_rangeslider_visible=True)
plot(iterative_figure)