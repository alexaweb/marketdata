# Standard library imports
import argparse
from datetime import datetime, time, timedelta
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from lxml import html
import re
import requests
import pandas as pd

# Third party imports
from bs4 import BeautifulSoup

# Local application imports
import config
from include.librarycurrencies import getcurrencies
from include.writetodb import writePriceToDb

parser = argparse.ArgumentParser(description='NOTE: arguments required')
parser.add_argument("--b", required=True, type=str,help="bucket name")
parser.add_argument("--o", required=True, type=str,help="organization name")
args = parser.parse_args()
bucket = args.b
org = args.o




d = getcurrencies()
#print(d)
print(d['usd_obs'])




midnight = datetime.combine(datetime.today(), time.min)
yesterday=midnight-timedelta(days=1)
print("date:",midnight)
print("yesterday:",yesterday)

ticker = "USDCLP"
q = influxdb_client.Point("price").tag("ticker",ticker).field("obs",d['usd_obs']).time(midnight)
#q = influxdb_client.Point("price").tag("ticker",ticker).field("obs",float(usd_obs)).time(yesterday)
writePriceToDb(q,bucket,org,config.url,config.token)

ticker = "EURCLP"
q = influxdb_client.Point("price").tag("ticker",ticker).field("close",d['eur']).time(midnight)
writePriceToDb(q,bucket,org,config.url,config.token)

ticker = "UFCLP"
q = influxdb_client.Point("price").tag("ticker",ticker).field("close",d['uf']).time(midnight)
writePriceToDb(q,bucket,org,config.url,config.token)

ticker = "Cu"
q = influxdb_client.Point("price").tag("ticker",ticker).field("close",d['cu']).time(midnight)
writePriceToDb(q,bucket,org,config.url,config.token)

ticker = "Au"
q = influxdb_client.Point("price").tag("ticker",ticker).field("close",d['au']).time(midnight)
writePriceToDb(q,bucket,org,config.url,config.token)

ticker = "Ag"
q = influxdb_client.Point("price").tag("ticker",ticker).field("close",d['ag']).time(midnight)
writePriceToDb(q,bucket,org,config.url,config.token)
