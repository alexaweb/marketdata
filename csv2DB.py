#######################
# ticker given as command line input
#
# CSV file must have single heading row with
# 'date' column formatted yyyy-mm-ddT00:00:00
# 'close' column with close market Value
#######################

# Standard library imports
import argparse
import csv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import re
import requests

# Third party imports

# Local application imports
import config
from include.writetodb import writePriceToDb


parser = argparse.ArgumentParser(description='NOTE: arguments required')
parser.add_argument("--t", required=True, type=str,help="ticker symbol")
parser.add_argument("--f", required=True, type=str,help="text filename with financial data for ticker symbol, one line per date. First row must be column headers and 'date' column header must exist")
parser.add_argument("--c", required=True, type=str,help="column to be read - should equal the name of the header")
parser.add_argument("--b", required=True, type=str,help="bucket name")
parser.add_argument("--o", required=True, type=str,help="organization name")


args = parser.parse_args()
ticker = args.t
filename = args.f
column = args.c
bucket = args.b
org = args.o


#bucket="testbucket"
#org="testorg"
#ticker="CFIBTGCYFA.SN"
#url = 'https://www.btgpactual.cl/fondo-de-inversion/credito-y-facturas/'
with open(filename,encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row['ticker']," fecha: ",row['date']," close: ",row['close'])
        print(ticker," fecha: ",row['date']," ",column,": ",row[column])
        #exit()
        q = influxdb_client.Point("price").tag("ticker",ticker).field(column,float(row[column])).time(row['date'])
        writePriceToDb(q,bucket,org,config.url,config.token)



exit()
