import pandas as pd
from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay


class BankHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Year', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        Holiday('Good Friday', month=1, day=1, offset=[Easter(), Day(-2)]),
        USMemorialDay,
        USLaborDay,
        USThanksgivingDay,
        Holiday('July 4th', month=7, day=4, observance=nearest_workday),
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]


marketCalendar = BankHolidayCalendar()
holidays = marketCalendar.holidays(start='2021-01-01', end='2024-12-31')
print(holidays.strftime("%Y-%m-%d").tolist())
