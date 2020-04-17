# Standard library imports
import argparse
from datetime import datetime, time, timedelta
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import re
import requests

# Third party imports
from bs4 import BeautifulSoup

# Local application imports
import config
from include.isnumber import is_number
from include.librarycurrencies import getcurrencies
from include.writetodb import writePriceToDb



parser = argparse.ArgumentParser(description='NOTE: arguments required')
#parser.add_argument("--f", required=True, type=str,help="text filename with ticker symbols, one per line be supplied")
parser.add_argument("--b", required=True, type=str,help="bucket name")
parser.add_argument("--o", required=True, type=str,help="organization name")
args = parser.parse_args()
#filename = args.f
bucket = args.b
org = args.o

#bucket="testbucket"
#org="testorg"

d = getcurrencies()
usd_obs = d['usd_obs']

#url = 'https://www.moneda.cl/private/valores-cuota'
url = 'https://www.moneda.cl/?switch=private'
page = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')
results = soup.find(id='tab-1')


fundticker_list = ['CFIPIONERO.SN','CFIMLDL.SN','CFIMRCLP']
fundname_list = ['Pionero','Moneda Latinoamérica Deuda Local (Serie A)','Moneda Renta CLP']
d = {'fundtickers': fundticker_list,'fundnames': fundname_list}
print(d)

n_rows=0
n_columns=2
for row in results.find_all('tr'):
    td_tags=row.find_all('td')
    if(len(td_tags))>0:
        n_rows+=1

new_table = pd.DataFrame(columns=range(0,n_columns),index=range(0,n_rows))
row_marker=0
for row in results.find_all('tr'):
    column_marker=0
    columns=row.find_all('td')
    for column in columns:
        new_table.iat[row_marker,column_marker]=column.get_text()
        column_marker+=1
    row_marker+=1

choices = {'Pionero':'CFIPIONERO.SN','Moneda Latinoamérica Deuda Local (Serie A)':'CFIMLDL.SN','Moneda Renta CLP':'CFIMRCLP.SN'}

#print(new_table)
#print(d.items())
midnight = datetime.combine(datetime.today(), time.min)
yesterday=midnight-timedelta(days=1)
print("yesterday:",yesterday)
insertdate = yesterday
#print(midnight)
for i in range(row_marker):
    fund_name=new_table[0][i].strip()
    test_string=new_table[1][i].strip()
    currency=test_string[0:3]
    value=float((test_string[3:].replace(".","")).strip().replace(",","."))
    print("Fondo:",fund_name,"; Moneda:",currency,";Valor Cuota:",value)
    ticker=choices.get(fund_name,0)
    if ticker != 0:
        print("yes:",value,insertdate,currency)
        q = influxdb_client.Point("price").tag("ticker",ticker).tag("name",fund_name).tag("currency",currency).field("nav",value).time(insertdate)
        writePriceToDb(q,bucket,org,config.url,config.token)
        if currency == "USD" and is_number(usd_obs):
            value=value*usd_obs
            print("value clp:",value,"date:",insertdate)
            q = influxdb_client.Point("price").tag("ticker",ticker).tag("name",fund_name).tag("currency","CLP").field("nav",value).time(insertdate)
            writePriceToDb(q,bucket,org,config.url,config.token)
