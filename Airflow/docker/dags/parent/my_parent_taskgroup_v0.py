from airflow import DAG
from airflow.operators.bash import BashOperator
from groups.my_parent_taskgroup_v0 import task_group_process
from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'schedule_interval': '@daily',
}

dag_id = "my_parent_taskgroup_v0.0"

with DAG(
    dag_id=dag_id, 
    default_args=default_args,
    tags=['parent'],
    catchup=False,
) as dag:

    start = BashOperator(
        task_id='start',
        bash_command='echo "Start"',
    )

    group_process1 = task_group_process(
        'group_process1', 
        {'process_a': 1, 'process_b': 2, 'process_c': 3, 'publish_a': 10, 'publish_b': 20, 'publish_c': 30})
    
    group_process2 = task_group_process(
        'group_process2', 
        {'process_a': 4, 'process_b': 5, 'process_c': 6, 'publish_a': 40, 'publish_b': 50, 'publish_c': 60})

    group_process3 = task_group_process(
        'group_process3', 
        {'process_a': 7, 'process_b': 8, 'process_c': 9, 'publish_a': 70, 'publish_b': 80, 'publish_c': 90})
            
    end = BashOperator(
        task_id='end',
        bash_command='echo "End"',
    )
    
    start >> [group_process1, group_process2, group_process3] >> end
