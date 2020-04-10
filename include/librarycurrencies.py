import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
# Standard library imports
from datetime import datetime, time, timedelta
from lxml import html

# Third party imports

# Local application imports
from .isnumber import is_number

def getcurrencies():
    url = 'https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx'
    d = dict()

    page = requests.get(url,verify=False)
#soup = BeautifulSoup(page.content,'html.parser')
    soup = BeautifulSoup(page.content,'lxml')
    usd_obs  = soup.find('label',id='lblValor1_3')
    usd_obs = usd_obs.contents[0]
    usd_obs = usd_obs.replace(".","")
    usd_obs = usd_obs.replace(",",".")
    if is_number(usd_obs):
        usd_obs = float(usd_obs)


    uf  = soup.find('label',id='lblValor1_1')
    uf = uf.contents[0]
    uf = uf.replace(".","")
    uf = uf.replace(",",".")
    if is_number(uf):
        uf = float(uf)

    eur  = soup.find('label',id='lblValor1_5')
    eur = eur.contents[0]
    eur = eur.replace(".","")
    eur = eur.replace(",",".")
    if is_number(eur):
        eur = float(eur)

    cu  = soup.find('label',id='lblValor2_5')
    cu = cu.contents[0]
    cu = cu.replace(".","")
    cu = cu.replace(",",".")
    if is_number(cu):
        cu = float(cu)

    au  = soup.find('label',id='lblValor2_3')
    au = au.contents[0]
    au = au.replace(".","")
    au = au.replace(",",".")
    if is_number(au):
        au = float(au)

    ag  = soup.find('label',id='lblValor2_4')
    ag = ag.contents[0]

    ag = ag.replace(".","")
    ag = ag.replace(",",".")
    if is_number(ag):
        ag = float(ag)
#print(usd)
#print(usd.contents)
#print(usd.contents[0])
    print("USDCLP observado:",usd_obs)
    print("UF:",uf)
    print("EUR:",eur)
    print("Cu:",cu)
    print("Au:",au)
    print("Ag:",ag)
    d['usd_obs']= usd_obs
    d['uf'] = uf
    d['eur'] = eur
    d['cu'] = cu
    d['au'] = au
    d['ag'] = ag

    return d
