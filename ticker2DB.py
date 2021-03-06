# ticker2DB.py
#
# input: filename bucket organization
# output: reads ticker symbols from filename and
#         writes ticker value (yahoo finance) to influxDB (bucket and organization)
#########################################
# Standard library imports
import argparse

# Third party imports

# Local application imports
import config
from include.finance import getTickerPrice
from include.writetodb import writePriceToDb

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

f=open(filename,'r')
while True:
    x=f.readline()
    if len(x.strip()) > 0:
        q = getTickerPrice(x.strip())
        if q is not None:
            print(q)
            writePriceToDb(q,bucket,org,config.url,config.token)
    else:
        exit()
        