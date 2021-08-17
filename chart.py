import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
import mplfinance as mpf
from tiingo import TiingoClient
from datetime import datetime, timedelta

# print((datetime.today() - timedelta(days=5)).date()) # gets the date 5 days before today


chartDays = 10
timeDiff = 6

ticker = input('Enter a ticker ').upper()

key = open('api_key.txt').read()
config = {}

config['session'] = True
config['api_key'] = "8e0be47061fc0cc55149cd88aa4aa5843e31b4c8"

client = TiingoClient(config)

priceData = client.get_dataframe(ticker, startDate='2021-08-10', endDate='2021-08-16', frequency='1min')
print(priceData.head())

priceData.columns = ['close', 'high', 'low', 'open']

priceData['TradeDate'] = priceData.index.date
priceData['time'] = priceData.index.time

# Adjusts times for different time zones
priceData['date'] = priceData.index - timedelta(hours=timeDiff)
priceData.sort_index(inplace=True)

# priceData = priceData.loc[(datetime.today() - timedelta(days=chartDays)).date():]  # picks start date of data

# Create subplots and mention plot grid size


"""
 fig.add_trace(go.Bar(x=priceData['date'], y=priceData['volume'], showlegend=False, marker_color='rgb(255,255,255)'),
             row=2, col=1)   
             #adds volume sublot below
"""
# Creating the candlestick chart without volume subplot


fig = go.Figure(data=[go.Candlestick(x=priceData['date'], open=priceData['open'], high=priceData['high'],
                                     low=priceData['low'], close=priceData['close'])])

fig.update_xaxes(
    rangeslider_visible=False,
    rangebreaks=[
        # NOTE: Below values are bound (not single values), ie. hide x to y
        dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
        dict(bounds=[14, 7.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
        # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
    ]
)

fig.update_layout(title=ticker + ' Analysis', template='plotly_dark', yaxis_title=ticker + " price (USD)")
fig.show()
