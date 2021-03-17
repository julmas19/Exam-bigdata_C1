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
meses=['enero','febrero','marzo','abril']
def f1(event,context):
  s3 = boto3.client('s3')
  c = (event['Records'][0]['s3']['object'])
  #print(a['s3']['object']['key'])
  key1 = c['key']
  key = c['key'].split('/')[2]
  time = (event['Records'][0]['eventTime']).split('.')[0]
  key_name = key.split('.')[0]
  ext_type = key.split('.')[1]
  #key_name = a['key'].split('.')[0]
  #ext_type = a['key'].split('.')[1]
  #namekey = a['key'].split('-')[0]
  new_ubi = '/tmp/{}'.format(key)
  new_name = '{}.csv'.format(key_name)
  ahora = datetime.now()
  s3.download_file("julianbucket24",key1,new_ubi)
  df = pd.read_csv(new_ubi, sep='\001')
 
  for i in range(len(df['enlace'])):
    url = df['enlace'][i]
    namenot = df['titular'][i]
    try:
      r = requests.get(url)
      doc = open("/tmp/doc.txt","w")
      doc.write(r.text)
      doc.close()
      s3.upload_file("/tmp/doc.txt","bucketnoticias","news/raw/periodico={}/year={}/month={}/day={}/{}.html".format(key_name,ahora.year,meses[ahora.month-1],ahora.day,namenot))
      
    except:
      None
