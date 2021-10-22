import key
from tiingo import TiingoClient
import pandas as pd
import market_holidays
from datetime import datetime, timedelta

api_key = key.api_key
config = {'session': True, 'api_key': api_key}
client = TiingoClient(config)
timeDiff = 6


ticker = "AMC"

# price_data = client.get_dataframe(ticker, startDate=(datetime.today()).strftime("%m/%d/%Y"),
#                                  endDate=datetime.today().strftime("%m/%d/%Y"), frequency='1min')

price_data = client.get_dataframe(ticker, start_date, end_date,
                                 frequency='1min')

price_data.index = price_data.index - timedelta(hours=timeDiff)

chartCalendar = market_holidays.Calendar("2020-01-01", "2021-12-31")
holidayDates = chartCalendar.get_holidays()

with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(price_data)

