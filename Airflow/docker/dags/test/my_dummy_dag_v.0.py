from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id='my_dummy_dag_v_0', 
    default_args=default_args,
    tags=['test'],
    schedule_interval='@daily',
    catchup=False,
    
) as dag:

    task1 = BashOperator(
        owner='mark',
        task_id='task1',
        bash_command='echo "Task 1"',
    )
    
    task2 = BashOperator(
        owner='mark',
        task_id='task2',
        bash_command='echo "Task 2"',
    )
    
    dummy = DummyOperator(
        task_id='dummy',
    )
    
    task3 = BashOperator(
        owner='mark',
        task_id='task3',
        bash_command='echo "Task 3"',
    )
    
    task4 = BashOperator(
        owner='mark',
        task_id='task4',
        bash_command='echo "Task 4"',
    )
    
    [ task1 , task2] >> dummy >> [ task3 , task4]
    