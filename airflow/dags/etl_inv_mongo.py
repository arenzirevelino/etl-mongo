import os
import json
import pandas as pd 
import sqlite3
from mongoConnectionFile import Connect
from sqlalchemy import create_engine
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
	'owner':'renzi',
	'email':'renzivelino@gmail.com',
	'email_on_failure':True,
	}

dag = 	DAG(
	'etl_to_mongodb',
	default_args = default_args,
	schedule_interval = None,
	start_date = days_ago(1),
	)

LOCAL_DATA_SOURCE = str(os.path.abspath('../../'+'data/chinook.db'))
FILE_OUTPUT = str(os.path.abspath('../../'+'data/chinook_invoice_csv.json'))
SQL_QUERY = str(os.path.abspath('../../'+'data/invoice_by_sales.sql'))

#Mongo Connection
client = Connect.getConnection() #Connect to MongoDB Cloud on Atlas Cluster
db_name = client.etl_mongo  #database name
Collection = db_name['invoice_sales'] #collection name

def extract_transform(**kwargs):
    ti = kwargs['ti']
    output_json = FILE_OUTPUT
    conn_local = sqlite3.connect(LOCAL_DATA_SOURCE)

    with open(SQL_QUERY, "r") as sql_query:
        df = pd.read_sql(sql_query.read(), conn_local)
        #transform result to json
        df.to_json(output_json, orient='records')
        ti.xcom_push('chinook_json', output_json)

def load(**kwargs):
    ti = kwargs['ti']
    jsonFile = ti.xcom_pull(task_ids='extract_transform', key='chinook_json')

    with open(jsonFile) as file_json:
        json_data = json.load(file_json)
    
    Collection.insert_many(json_data)


start = DummyOperator(
		task_id='start',
		dag = dag)

end	= DummyOperator(
		task_id='end',
		dag = dag)

extract_transform_task = PythonOperator(task_id='extract_transform',
			python_callable = extract_transform,
			dag = dag)

load_task = PythonOperator(task_id='load',
			python_callable = load,
			dag = dag)

start >> extract_transform_task >> load_task >> end