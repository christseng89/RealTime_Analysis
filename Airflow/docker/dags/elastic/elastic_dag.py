from airflow import DAG
from airflow.operators.python import PythonOperator
from hooks.elastic.elastic_hook import ElasticHook 
from pprint import pprint  
from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def _print_es_info():
    hook = ElasticHook()
    print ("Elasticsearch info:")
    pprint(hook.info())

with DAG(
    dag_id='elastic_dag', 
    default_args=default_args, 
    schedule_interval='@daily', 
    catchup=False) as dag:

    print_es_info = PythonOperator(
        task_id='print_es_info',
        python_callable=_print_es_info
    )
