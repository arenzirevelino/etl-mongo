import os
import json
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

LOCAL_DATA_SOURCE = str(os.path.abspath('../../'+'/data/chinook.db'))
FILE_OUTPUT = str(os.path.abspath('../..'+'/data/chinook_invoice_csv.json'))
SQL_QUERY = str(os.path.abspath('../..'+'/data/invoice_by_sales.sql'))

def extract_transform_data(**kwargs):
    ti = kwargs['ti']
    output_json = FILE_OUTPUT
    conn_local = sqlite3.connect(LOCAL_DATA_SOURCE)

    with open(SQL_QUERY, "r") as sql_query:
        df = pd.read_sql(sql_query.read(), conn_local)
        #transform result to json
        df.to_json(output_json, orient='records')
        ti.xcom_push('chinook_json', output_json)