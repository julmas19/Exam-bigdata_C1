import json
import boto3
import re
from io import StringIO
from datetime import datetime, timedelta
import requests
import pandas as pd
import urllib.request
import time
from bs4 import BeautifulSoup
import ast

def f1(event, context):
 class YahooFinanceHistory:
    timeout = 2
    crumb_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{quote}?period1={dfrom}&period2={dto}&interval=1d&events=history&crumb={crumb}'

    def __init__(self, symbol, days_back=0):
        self.symbol = symbol
        self.session = requests.Session()
        self.dt = timedelta(days=days_back)

    def get_crumb(self):
        response = self.session.get(self.crumb_link.format(self.symbol), timeout=self.timeout)
        response.raise_for_status()
        match = re.search(self.crumble_regex, response.text)
        if not match:
            raise ValueError('Could not get crumb from Yahoo Finance')
        else:
            self.crumb = match.group(1)

    def get_quote(self):
        if not hasattr(self, 'crumb') or len(self.session.cookies) == 0:
            self.get_crumb()
        now = datetime.utcnow()
        dateto = int(now.timestamp())
        datefrom = int((now - self.dt).timestamp())
        url = self.quote_link.format(quote=self.symbol, dfrom=datefrom, dto=dateto, crumb=self.crumb)
        response = self.session.get(url)
        response.raise_for_status()
        namefil = self.symbol
        filename = "/tmp/{}.txt".format(namefil)
        r = urllib.request.urlopen(url)
        f = open(filename,"wb")
        f.write(r.read())
        f.close()
        s3 = boto3.client('s3')
        newname = "{}.txt".format(namefil)
        s3.upload_file(filename,"julianbucket22",newname)
        return None

 YahooFinanceHistory('AVHOQ', days_back=5).get_quote()
 time.sleep(5)
 YahooFinanceHistory('EC', days_back=5).get_quote()
 time.sleep(5)
 YahooFinanceHistory('AVAL', days_back=5).get_quote()
 time.sleep(5)
 YahooFinanceHistory('CMTOY', days_back=5).get_quote()
 
 return {
    'statusCode': 200,
    'body': json.dumps(' ')
 }
def f2(event, context):
 s3 = boto3.client('s3')
 ahora = datetime.now()
 print("evento",event)
 papers = ['eltiempo','elespectador']
 
 for i in papers:
  name = '{}_{}_{}_{}'.format(i,ahora.year,ahora.month,ahora.day)
  r = requests.get('https://www.{}.com/'.format(i))
  doc = open("/tmp/doc.txt","w")
  doc.write(r.text)
  doc.close()
  meses = ['enero','febrero','marzo','abril']
  ruta = 'news/raw/periodico={}/year={}/month={}/day={}/{}.txt'.format(i,ahora.year,meses[ahora.month-1],ahora.day,name)
  s3.upload_file("/tmp/doc.txt","julianbucket23",ruta)
  s3.upload_file("/tmp/doc.txt","julianbucket23","news/raw/{}.txt".format(i))
