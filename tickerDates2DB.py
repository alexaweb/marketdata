# Standard library imports
import argparse

# Third party imports

# Local application imports
import config
from include.finance2DB import getTickerPriceDates2Db

parser = argparse.ArgumentParser(description='NOTE: arguments required')
parser.add_argument("--f", required=True, type=str,help="text filename with ticker symbols, one per line be supplied")
parser.add_argument("--b", required=True, type=str,help="bucket name")
parser.add_argument("--o", required=True, type=str,help="organization name")
parser.add_argument("--d1", required=True,type=str,help="start date")
parser.add_argument("--d2", required=True,type=str,help="end date")
args = parser.parse_args()
filename = args.f
bucket = args.b
org = args.o
date1 = args.d1
date2 = args.d2


f=open(filename,'r')
while True:
    x=f.readline()
    if len(x.strip()) > 0:
        getTickerPriceDates2Db(x.strip(),bucket,org,date1,date2,config.url,config.token)
    else:
        exit()
