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

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "MEME  STOCK TRADER"

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}
app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [

                        html.H4("AMC Stock Analysis", className="app__header__title"),
                        html.P(
                            "This app provides a real time chart for AMC moon stock.",
                            className="app__header__title--grey",
                        ),
                        dcc.Input(id='input-box', value='AMC', type='text', placeholder='Enter a stock ticker'),
                        html.Button('Enter', id='enter_button'),
                    ],
                    className="app__header__desc"
                ),
            ],
            className="app__header"
        ),
        html.Div(
            [
                # stock price
                html.Div(
                    [
                        html.Div(
                            [html.H6("AMC", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="stock-price",
                            # animate=True,
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"]
                                )
                            )
                        ),
                        dcc.Interval(
                            id="chart-update",
                            interval=1 * 30000,
                            n_intervals=0
                        )
                    ],
                    className="two-thirds column stock__price__container"
                ),
            ],
            className="app__content"
        )
    ],
    className="app__container"
)

api_key = key.api_key
config = {'session': True, 'api_key': api_key}
client = TiingoClient(config)
timeDiff = 6


# chartFrequency = '5min'

@app.callback(
    Output('stock-price', 'figure'),
    [Input('chart-update', 'n_intervals'), Input('enter_button', 'n_clicks')],
    [State('input-box', 'value')]
)
def update_figure(interval, n_clicks, input_value):
    ticker = input_value.upper()
    price_data = client.get_dataframe(ticker, startDate=(datetime.today() - timedelta(days=3)).strftime("%m/%d/%Y"),
                                      endDate=datetime.today().strftime("%m/%d/%Y"), frequency='1min')

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
