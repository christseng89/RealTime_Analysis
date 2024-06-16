from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator

from subdags.my_parent_subdag_v1 import subdag_processes

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'schedule_interval': '@daily',
}

dag_id = "my_parent_subdag_v1.0"

with DAG(
    dag_id=dag_id, 
    default_args=default_args,
    catchup=False,
) as dag:

    start = BashOperator(
        task_id='start',
        bash_command='echo "Start"',
    )

    group_process = SubDagOperator(
        task_id='group_process',
        subdag=subdag_processes(
            dag_id,
            'group_process',
            default_args,
        ),
        mode='reschedule',
        timeout=60,
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "End"',
    )
    
    start >> group_process >> end
    