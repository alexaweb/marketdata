# Standard library imports
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Third party imports
import yfinance as yf

def getTickerPrice(ticker):

    stock = yf.Ticker(ticker)
    stock_yesterday=stock.history(period="1d")
    if stock_yesterday.empty:
            return

    print("=============")
    print("ticker:",ticker)
    print(stock_yesterday)
    dictionary_stock_yesterday = stock_yesterday.to_dict('records')
    field_string=dictionary_stock_yesterday[0]
    time_string=str(stock_yesterday.index.values[0])
    time_string=time_string[:-3]
    print(time_string)
    utc_time = datetime.strptime(time_string,"%Y-%m-%dT%H:%M:%S.%f")
    utc_time=int(utc_time.timestamp())
    open = float(field_string['Open'])
    high = float(field_string['High'])
    low = float(field_string['Low'])
    close = float(field_string["Close"])
    volume = float(field_string['Volume'])

    q = influxdb_client.Point("price").tag("ticker",ticker).field("close",close).field("high",high).field("low",low).field("open",open).field("volume",volume).time(time_string)
    return q
