from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'schedule_interval': None, ## Need to run Dag via TriggerDagRunOperator
}

dag_id = "my_parent_target_v0"

with DAG(
    dag_id=dag_id, 
    default_args=default_args,
    catchup=False,
) as dag:

    test1 = BashOperator(
        task_id='test1',
        bash_command='echo "Test1" && echo "{{ dag_run.conf["process_a"]}} "',
    )
    
    test2 = BashOperator(
        task_id='test2',
        bash_command='echo "Test2" && echo "{{ dag_run.conf["process_b"]}} "',
    )
    
    test3 = BashOperator(
        task_id='test3',
        bash_command='echo "Test3" && echo "{{ dag_run.conf["process_c"]}} "',
    )
    
    test1 >> test2 >> test3
    