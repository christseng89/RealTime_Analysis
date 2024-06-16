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
    'catchup': False,
}

with DAG(
    dag_id='my_parent_dag_v1.0', 
    default_args=default_args,
) as dag:

    start = BashOperator(
        task_id='start',
        bash_command='echo "Start"',
    )

    group_process = SubDagOperator(
        task_id='group_process',
        subdag=subdag_processes(
            'my_parent_dag_v1.0',
            'group_process',
            default_args,
        ),
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "End"',
    )
    
    start >> group_process >> end
    