# readtickerfrom2DB.py
#
# input: bucket and organization
# output: reads ticker values for 366 days past and writes to google sheet
#########################################
# Standard library imports
import argparse

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import pandas as pd

# Third party imports

# Local application imports
import config
##from include.finance import getTickerPrice
from include.readfromdb import readFromDB, readFromDBworks

parser = argparse.ArgumentParser(description='NOTE: arguments required')
parser.add_argument("--f", required=True, type=str,help="text filename with ticker symbols, one per line be supplied")
parser.add_argument("--b", required=True, type=str,help="bucket name")
parser.add_argument("--o", required=True, type=str,help="organization name")
args = parser.parse_args()
filename = args.f
bucket = args.b
org = args.o

#bucket = "testbucket"
#org = "testorg"


#readFromDBworks("MRCLP",bucket,org,config.url,config.token)

data = readFromDB(15,bucket,org,config.url,config.token)

print(data)
df = pd.DataFrame(data,columns =['fecha','ticker','valor','close'])


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ubuntu/apps/marketdata/client_secret_interpetrol.json', scope)
client = gspread.authorize(creds)
file_id = '1p62PeXYqs2rLbs7BlpsLWzLeq2zHWbfWZlXedDlz_mQ'



ws = client.open_by_key(file_id)
sh = ws.worksheet("GRAFANA")
sh.clear()
set_with_dataframe(sh,df)        