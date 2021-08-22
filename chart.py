import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import key
from tiingo import TiingoClient
import pandas as pd
import plotly.graph_objs as go
import market_holidays
from datetime import datetime, timedelta

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://codepen.io/chriddyp/pen/bWLwgP.css'
    ),
    dcc.Input(id='input-box', value='SPY', type='text', placeholder='Enter a stock ticker'),
    html.Button('Enter', id='enter_button'),
    html.Div(),
    html.P('4 Searches per Minute'),
    dcc.Graph(id='candle-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}, ),
    dcc.Interval(
        id='interval-component',
        interval=1 * 60000,  # in milliseconds
        n_intervals=0),
    html.Div([
        html.P('Developed by: ', style={'display': 'inline', 'color': 'white'}),
        html.A('Kaden Baskett', href='https://kadenbaskett.wixsite.com/mysite'),
        html.P(' - ', style={'display': 'inline', 'color': 'white'}),
        html.A('kadenbaskett@gmail.com', href='mailto:kadenbaskett@gmail.com')
    ], className="twelve columns",
        style={'fontsize': 18, 'padding-top': 20}
    ),
])

api_key = key.api_key
config = {'session': True, 'api_key': api_key}
client = TiingoClient(config)
timeDiff = 6


# chartFrequency = '5min'


@app.callback(
    Output('candle-graph', 'figure'),
    [Input('enter_button', 'n_clicks'), Input('interval-component', 'n_intervals')],
    state=[State(component_id='input-box', component_property='value')]
)
def update_figure(n, In_clicks, input_value):
    ticker = input_value.upper()
    price_data = client.get_dataframe(ticker, startDate="2021-08-19",
                                      endDate="2021-08-24", frequency='1min')

    price_data.index = price_data.index - timedelta(hours=timeDiff)

    chartCalendar = market_holidays.Calendar("2020-01-01", "2021-12-31")
    holidayDates = chartCalendar.get_holidays()

    fig = go.Figure(go.Candlestick(
        x=price_data.index,
        open=price_data['open'],
        high=price_data['high'],
        low=price_data['low'],
        close=price_data['close']

    ))

    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[14, 7.5], pattern="hour"),
            dict(values=holidayDates)
        ]
    )

    fig.update_layout(title=ticker + " Analysis", template='plotly_dark', yaxis_title=ticker + " price (USD)")

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
