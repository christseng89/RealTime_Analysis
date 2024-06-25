from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook
from datetime import datetime

default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 5, 1),
    'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def test_elastic_connection():
    hook = HttpHook(
        http_conn_id='elastic_default', 
        method='GET')
    response = hook.run('/')
    print(response.text)

with DAG(
    dag_id='test_elastic_connection_dag', 
    default_args=default_args,
    schedule_interval='@daily', 
    tags=['elastic'],
    catchup=False) as dag:

    test_connection = PythonOperator(
        task_id='test_connection',
        python_callable=test_elastic_connection,
    )
