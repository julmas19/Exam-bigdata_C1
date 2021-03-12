import json
import boto3
import re
from io import StringIO
from datetime import datetime, timedelta
import requests
import pandas as pd
import urllib.request
import time
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
        s3.upload_file(filename,"julianbucket19",newname)
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
