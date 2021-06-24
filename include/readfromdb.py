# Standard library imports
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Third party imports

# Local application imports


def writePriceToDb(string,bucket,org,url,token):
 ##   influxdbtoken="X404O4n501Am7WC3HJbK-X-UBEwAdU1Y2VxickrCvdcOhHGV6CGWpbHOQAHZeT9-cK2LNm-b5nZqc0LXQfQ86w=="
  ##  influxdburl="http://localhost:9999"
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=bucket, org=org, record=string)


def readFromDBworks(string,bucket,org,url,token):
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org) 
    query_api = client.query_api()
    query = 'from(bucket:"market")\
    |> range(start: -10d)'
    ## Using Table Structure
    result = query_api.query(org=org, query=query)
    results = []

    for table in result:
        for record in table.records:
            print (record.values)

def readtickerFromDB(string,bucket,org,url,token):
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org) 
    query_api = client.query_api()
    query = 'from(bucket:"'+bucket+'")\
    |> range(start: -366d)\
    |> filter(fn:(r) => r.ticker == "'+string+'")\
    |> filter(fn:(r) => r._field == "close")'
    ## Using Table Structure
    print(query)
    result = query_api.query(org=org, query=query)
    results = []

    for table in result:
        for record in table.records:
            print (record.values)

def readFromDB(days,bucket,org,url,token):
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org) 
    query_api = client.query_api()
    query = 'from(bucket:"'+bucket+'")\
    |> range(start: -'+str(days)+'d)\
    |> filter(fn:(r) => r._field == "close")'
    ## Using Table Structure
    print(query)
    result = query_api.query(org=org, query=query)
    results = []

    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.values.get("ticker"),record.get_field(),record.get_value()))

    print(results)