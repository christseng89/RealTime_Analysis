from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id='my_parent_subdag_v0.0', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['parent'],
    catchup=False,
) as dag:

    start = BashOperator(
        task_id='start',
        bash_command='echo "Start"',
    )

    process_a = BashOperator(
        task_id='process_a',
        bash_command='echo "Process A"',
    )
    
    process_b = BashOperator(
        task_id='process_b',
        bash_command='echo "Process B"',
    )
    
    process_c = BashOperator(
        task_id='process_c',
        bash_command='echo "Process C"',
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "End"',
    )
    
    start >> [process_a, process_b, process_c] >> end
    