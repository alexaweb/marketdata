# Standard library imports
import argparse

# Third party imports

# Local application imports
import config
from include.finance2DB import getTickerPriceHistory2Db

parser = argparse.ArgumentParser(description='NOTE: arguments required')
parser.add_argument("--f", required=True, type=str,help="text filename with ticker symbols, one per line be supplied")
parser.add_argument("--b", required=True, type=str,help="bucket name")
parser.add_argument("--o", required=True, type=str,help="organization name")
args = parser.parse_args()
filename = args.f
bucket = args.b
org = args.o


f=open(filename,'r')
while True:
    x=f.readline()
    if len(x.strip()) > 0:
        getTickerPriceHistory2Db(x.strip(),bucket,org,config.url,config.token)
    else:
        exit()
