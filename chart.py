import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import datetime as dt
import mplfinance as mpf
from datetime import datetime, timedelta

# print((datetime.today() - timedelta(days=5)).date()) # gets the date 5 days before today

ticker = input('Enter a ticker ').upper()
key = open('api_key.txt').read()

"""
ta = TechIndicators(key, output_format='pandas')
rsiData, taMeta = ta.get_rsi(ticker, interval='1min', time_period=60, series_type='close')
"""

ts = TimeSeries(key, output_format='pandas')
"""
priceData, tsMeta = ts.get_daily(ticker, outputsize='full')
***For getting daily stock candles***
"""

priceData, tsMeta = ts.get_intraday(ticker, interval='5min', outputsize='full')
# ***For getting daily stock candles***

priceData.columns = ['open', 'high', 'low', 'close', 'volume']
priceData['TradeDate'] = priceData.index.date
priceData['time'] = priceData.index.time
priceData['date'] = priceData.index
priceData.sort_index(inplace=True)

priceData = priceData.loc[(datetime.today() - timedelta(days=5)).date():]  # picks start date of data
# priceData['20wma'] = priceData['close'].rolling(window=140).mean()  # Creates 20 day moving average from the dail candles uses140 because 20 week x 7 day/week = 140

fig = go.Figure(data=[go.Candlestick(x=priceData['date'], open=priceData['open'], high=priceData['high'],
                                     low=priceData['low'], close=priceData['close'])])
# fig.add_trace(go.Scatter(x=priceData['TradeDate'], y=priceData['20wma'], line=dict(color='#e0e0e0'), name="20 Week Moving Average"))

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=['sat', 'mon'])
        # hide weekends
    ]
)

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=[20, 4], pattern='hour')
        # hide non market hours
    ]
)

fig.update_layout(xaxis_rangeslider_visible=False, template='plotly_dark')
fig.update_layout(yaxis_title=ticker + " price (USD)", xaxis_title="Time")
fig.show()

"""
colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')
mpfStyle = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
mpf.plot(priceData, type="candle", style=mpfStyle, volume=True)
"""

"""
columns = ['open', 'high', 'low', 'close', 'volume']
priceData.columns = columns
priceData['TradeDate'] = priceData.index.date
priceData['time'] = priceData.index.time

# print(data.loc['2021-7-16'])

market = priceData.between_time('07:30:30', '14:00:00').copy()
market.sort_index(inplace=True)
# print(market.info())
# print(market.groupby('TradeDate').agg({'low':min, 'high':max}))       gets high & low
# print(market.loc[market.groupby('TradeDate')['low'].idxmin()])      shows time stamp of the daily lows with the high,open and other data shown at that same time stamp
# print(market.loc[market.groupby('TradeDate')['low'].idxmax()])    # same as above but for max """
