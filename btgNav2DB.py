# Standard library imports
import argparse
from datetime import datetime, time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from lxml import html
import pandas as pd
import requests
import re

# Third party imports
from bs4 import BeautifulSoup

# Local application imports
import config
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
ticker="CFIBTGCYFA.SN"
url = 'https://www.btgpactual.cl/fondo-de-inversion/credito-y-facturas/'

#pattern = re.compile(r"currentValue\":(\d+.\d+)")
#pattern_date = re.compile(r"lasUpdate\":\"(\d{4}-\d{2}-\d{2})")
pattern_last_entry = re.compile(r"var jsonFondos = '(.+)';")

page = requests.get(url,verify=False)
#soup = BeautifulSoup(page.content,'html.parser')
soup = BeautifulSoup(page.content,'lxml')
scripts  = soup.find_all("script")
for script in scripts:
    values=re.findall(r'\d+',str(script))
#    search_result=pattern.search(str(script))
#    search_result_date=pattern_date.search(str(script))
#    print(search_result_date)
    search_result_last_entry=pattern_last_entry.search(str(script))
    #print(search_result.group())
    if search_result_last_entry is not None:
#        nav=float(search_result.group(1))
#        date=search_result_date.group(1)
        json_txt=search_result_last_entry.group(1)
#        print("nav:",nav)
#        print("date:",date)
#        print("sript:",script)
#        print("json:",json_txt)
        data = json.loads(json_txt)
#        print("only entries:",data['perf']['performance']['entry'])
        lastvalue = max(data['perf']['performance']['entry'],key=lambda item:item['key'])
        print(lastvalue)
        nav = lastvalue['value']
        date = lastvalue['key']
        print("nav:",nav)
        print("date:",date)
        date=datetime.strptime(date,"%Y-%m-%dT%H:%M:%S%Z:00")
        print('fecha2: ',date)        
             

q = influxdb_client.Point("price").tag("ticker",ticker).tag("currency","CLP").field("nav",nav).time(date)
writePriceToDb(q,bucket,org,config.url,config.token)
