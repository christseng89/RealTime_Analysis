from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator

from datetime import datetime
import yaml
import os

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def _check_holidays(ds, **kwargs):
    file_path = os.path.join(os.path.dirname(__file__), 'files/days_off.yml')
    with open(file_path) as file:
        days_off = set(yaml.load(file, Loader=yaml.FullLoader))
        print("Days Off Info.: ", days_off)
        
    ds_date = datetime.strptime(ds, '%Y-%m-%d').date()
    print("DS: ", ds_date, "DS in Days Off: ", ds_date in days_off)
    
    if ds_date not in days_off:    
        return ['process', 'top_process']
   
    return 'stop'

with DAG(
    dag_id='my_branch_dag_v.1', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['branch'],
    catchup=True,
) as dag:

    ml_training = DummyOperator(
        owner='luke',
        task_id='ml_training',
    )

    check_holidays = BranchPythonOperator(
        task_id='check_holidays',
        python_callable=_check_holidays,
    )
    
    process = DummyOperator(
        task_id='process',
    )

    top_process = DummyOperator(
        task_id='top_process',
    )
    
    stop = DummyOperator(
        task_id='stop',
    )

    publish_ml = DummyOperator(
        task_id='publish_ml',
        trigger_rule='none_failed_min_one_success',
    )
    
    ml_training >> check_holidays >> [process, top_process, stop] 
    top_process >> publish_ml
    