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
