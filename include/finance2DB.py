# Standard library imports
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Third party imports
import yfinance as yf

# Local application imports
from include.writetodb import writePriceToDb


def getTickerPriceHistory2Db(ticker,bucket,org,url,token):

    stock = yf.Ticker(ticker)
    stock_history=stock.history(period="max")
    if stock_history.empty:
            return

    print("=============")
    print("ticker:",ticker)
    print(stock_history)
    num_records = len(stock_history)
    print("length:",num_records)

    for i in range(num_records):
        print("record:",i)
        dictionary_stock_history = stock_history.to_dict('records')
        field_string=dictionary_stock_history[i]
        time_string=str(stock_history.index.values[i])
        time_string=time_string[:-3]
        #print(time_string)
        utc_time = datetime.strptime(time_string,"%Y-%m-%dT%H:%M:%S.%f")
        utc_time=int(utc_time.timestamp())
        open = float(field_string['Open'])
        high = float(field_string['High'])
        low = float(field_string['Low'])
        close = float(field_string["Close"])
        volume = float(field_string['Volume'])

        q = influxdb_client.Point("price").tag("ticker",ticker).field("close",close).field("high",high).field("low",low).field("open",open).field("volume",volume).time(time_string)
        writePriceToDb(q,bucket,org,url,token)

def getTickerPriceDates2Db(ticker,bucket,org,date1,date2,url,token):

    #stock = yf.Ticker(ticker)
    #stock_history=stock.history(period="max")
    stock_history=yf.download(ticker,start=date1, end=date2)
    if stock_history.empty:
            return

    print("=============")
    print("ticker:",ticker)
    print(stock_history)
    num_records = len(stock_history)
    print("length:",num_records)

    for i in range(num_records):
        print("record:",i)
        dictionary_stock_history = stock_history.to_dict('records')
        field_string=dictionary_stock_history[i]
        time_string=str(stock_history.index.values[i])
        time_string=time_string[:-3]
        #print(time_string)
        utc_time = datetime.strptime(time_string,"%Y-%m-%dT%H:%M:%S.%f")
        utc_time=int(utc_time.timestamp())
        open = float(field_string['Open'])
        high = float(field_string['High'])
        low = float(field_string['Low'])
        close = float(field_string["Close"])
        volume = float(field_string['Volume'])

        q = influxdb_client.Point("price").tag("ticker",ticker).field("close",close).field("high",high).field("low",low).field("open",open).field("volume",volume).time(time_string)
        writePriceToDb(q,bucket,org,url,token)
