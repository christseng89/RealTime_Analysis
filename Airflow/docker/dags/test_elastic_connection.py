from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook
from datetime import datetime

def test_elastic_connection():
    hook = HttpHook(http_conn_id='elastic_default', method='GET')
    response = hook.run('/')
    print(response.text)

with DAG(
    dag_id='test_elastic_connection_dag', 
    start_date=datetime(2023, 1, 1), 
    schedule_interval='@daily', 
    catchup=False) as dag:

    test_connection = PythonOperator(
        task_id='test_connection',
        python_callable=test_elastic_connection,
    )
