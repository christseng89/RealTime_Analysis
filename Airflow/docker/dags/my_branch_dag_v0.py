from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def _check_accurate():
    accurate = 0.16
    if accurate > 0.15:
        return ['accurate', 'top_accurate']
   
    return 'inaccurate'

with DAG(
    dag_id='my_branch_dag_v.0', 
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    ml_training = DummyOperator(
        owner='luke',
        task_id='ml_training',
    )

    check_accurate = BranchPythonOperator(
        task_id='check_accurate',
        python_callable=_check_accurate,
    )
    
    accurate = DummyOperator(
        task_id='accurate',
    )

    top_accurate = DummyOperator(
        task_id='top_accurate',
    )
    
    inaccurate = DummyOperator(
        task_id='inaccurate',
    )

    publish_ml = DummyOperator(
        task_id='publish_ml',
        trigger_rule='none_failed_or_skipped',
    )
    
    ml_training >> check_accurate >> [accurate, top_accurate, inaccurate] >> publish_ml
