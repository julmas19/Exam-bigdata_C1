import boto3
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import ast
from datetime import datetime
pila=[]
meses = ['enero','febrero','marzo','abril']
def f1(event,context):
    s3 = boto3.client('s3')
    print("evento",event)
    eventos = event.keys()
    print('llaves',eventos)
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
    s3.download_file("julianbucket23",key1,new_ubi)
    if (key_name=="eltiempo"):
      y = []
      doc = open(new_ubi,'r')
      soup = BeautifulSoup(doc, 'lxml')
      line1 = open(new_ubi,"w")
      line1csv = open("/tmp/doc1sv.txt","w")
      div_main = soup.find_all("h3", {"class":"title-container"})
      cont = 0
      line1csv.write("categoria"+"\001"+"titular"+"\001"+"enlace"+"\n")
      for i in div_main:
        k = str(i)
        cont +=1
        tag = BeautifulSoup(k, 'html.parser').a
        try:
          h = tag['href']
          category = h.split('/')[1]
          content = tag.text
          url = ('https://www.eltiempo.com'+h)
          line1.write(category+"\001"+content+"\001"+url+"\n")
          line1csv.write(category+"\001"+content+"\001"+url+"\n")
        except:
          print("")
      doc.close()
      line1.close()
      line1csv.close()
      s3.upload_file(new_ubi,"julianbucket24","headlines/final/periodico={}/year={}/month={}/day={}/{}".format(key_name,ahora.year,meses[ahora.month-1],ahora.day,new_name))
      s3.upload_file("/tmp/doc1sv.txt","julianbucket24","headlines/final/{}".format(new_name))
      bucket_name = "athenalogsexam"
      client = boto3.client("athena")
      config = {
          "OutputLocation": "s3://" + bucket_name + "/",
          "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"}
      }

      # Query Execution Parameters
      sql = "alter table papers add partition(periodico='{}',year='{}',month='{}',day='{}')".format(key_name,ahora.year,meses[ahora.month-1],ahora.day)
      context = {"Database": "exam1"}
      respon = client.start_query_execution(QueryString = sql,
          QueryExecutionContext = context,
          ResultConfiguration = config)
      a = respon['QueryExecutionId']
      line.close()
      client.stop_query_execution(QueryExecutionId=a)
    if (key_name=="elespectador"):
      pila1=[]
      y1 = []
      dicc={}
      doc1 = open(new_ubi,'r')
      soup = BeautifulSoup(doc1, 'lxml')
      line = open("/tmp/doc.txt","w")
      linecsv = open("/tmp/docsv.txt","w")
      div_main1 = soup.find_all("script", {"type":"application/ld+json"})
      print(div_main1[2])
      linecsv.write("categoria"+"\001"+"titular"+"\001"+"enlace"+"\n")
      for i in div_main1:
       
        try:
          print(i,'esto es i')
          k = i.next
          print(k)
          dicc.update(ast.literal_eval(k.replace('""',"'")))
          y1.append(dicc)
          for i in y1:
            enl = i['mainEntityOfPage']['@id']
            cat = i['articleSection']
            tit = i['headline']
            line.write(cat+"\001"+tit+"\001"+enl+"\n")
            linecsv.write(cat+"\001"+tit+"\001"+enl+"\n")
          y1.pop()
        except:
          None
      doc1.close()     
      line.close()
      linecsv.close()
      s3.upload_file("/tmp/doc.txt","julianbucket24","headlines/final/periodico={}/year={}/month={}/day={}/{}".format(key_name,ahora.year,meses[ahora.month-1],ahora.day,new_name))
      s3.upload_file("/tmp/docsv.txt","julianbucket24","headlines/final/{}".format(new_name))
      bucket_name = "athenalogsexam"
      client = boto3.client("athena")
      config = {
          "OutputLocation": "s3://" + bucket_name + "/",
          "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"}
      }
    
      # Query Execution Parameters
      sql = "alter table papers add partition(periodico='{}',year='{}',month='{}',day='{}')".format(key_name,ahora.year,meses[ahora.month-1],ahora.day)
      context = {"Database": "exam1"}
      respon = client.start_query_execution(QueryString = sql,
          QueryExecutionContext = context,
          ResultConfiguration = config)
      a = respon['QueryExecutionId']
      line.close()  
      client.stop_query_execution(QueryExecutionId=a)

