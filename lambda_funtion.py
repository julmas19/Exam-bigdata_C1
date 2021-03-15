import json
import boto3
def lambda_handler(event, context):
     # TODO implement
    print('subido a s3')
    print('event',event)
    eventos = event.keys()
    print('llaves',eventos)
    a = (event['Records'][0]['s3']['object'])
    #print(a['s3']['object']['key'])
    key = a['key']
    time = (event['Records'][0]['eventTime']).split('.')[0]
    key_name = a['key'].split('.')[0]
    ext_type = a['key'].split('.')[1]
    new_ubi = '/tmp/{}'.format(key)
    new_name = '{}{}.csv'.format(key_name, time)
    s3 = boto3.client('s3')
    cont = 0
    if(ext_type == 'txt'):
        s3.download_file("julianbucket22", key, new_ubi)
        line = open(new_ubi, 'r')
        lineas = line.readlines()
        line.close()
        cont = 0
        line = open(new_ubi, 'w')
        size = len(lineas)
        for linea in lineas:
            if cont == (size-1) :
                line.write(linea)
                cont += 1
            else:
                cont += 1
        
        line = open(new_ubi, 'r')
        lineas = line.readlines()
        print(lineas)
        doc = lineas[0].split(',')[0].split('-')
        meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
        mes=meses[int(doc[1])-1]
        
        ubiex = "stocks/company={}/year={}/month={}/day={}/".format(key_name,doc[0],mes,doc[2])
        sintaxkey = 'stocks/company={}/year={}/month={}/day={}/{}'.format(key_name,doc[0],mes,doc[2],new_name)
        #s3.put_object(Bucket='bucketexam1bd', Key = sintaxkey)
        s3d = boto3.resource('s3')
        s3.put_object(Bucket='bucketexambd', Key = sintaxkey)
        objects_to_delete = s3d.meta.client.list_objects(Bucket="bucketexambd", Prefix=ubiex)
        delete_keys = {'Objects' : []}
        delete_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
        s3d.meta.client.delete_objects(Bucket="bucketexambd", Delete=delete_keys)
        #subida de archivo
        s3.upload_file(new_ubi,"bucketexambd",sintaxkey)
        bucket_name = "athenalogsexam"
        client = boto3.client("athena")
        config = {
            "OutputLocation": "s3://" + bucket_name + "/",
            "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"}
        }
        
        # Query Execution Parameters
        sql = "alter table company add partition(company='{}',year='{}',month='{}',day='{}')".format(key_name,doc[0],mes,doc[2])
        context = {"Database": "exam1"}
        respon = client.start_query_execution(QueryString = sql,
            QueryExecutionContext = context,
            ResultConfiguration = config)
        a = respon['QueryExecutionId']
        line.close()  
        client.stop_query_execution(QueryExecutionId=a)
    return {
        'statusCode': 200,
        'body': json.dumps(' ')
    }
