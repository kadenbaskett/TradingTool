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


# Creates custom holidays for all observed holiday dates by the U.S. stock market

marketCalendar = BankHolidayCalendar()


# Generates observed holiday dates by the U.S. stock market over a specified start and end date
class Calendar:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    # Returns the list of holiday dates
    def get_holidays(self):
        holidays = marketCalendar.holidays(start=self.start_date, end=self.end_date)
        return holidays.strftime("%Y-%m-%d").tolist()
