from airflow import DAG
from airflow.operators.bash import BashOperator

from groups.group_downloads import download_tasks
from groups.group_transforms import transform_tasks

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id='group_task', 
    # start_date=datetime(2023, 1, 1), 
    default_args=default_args,
    schedule_interval='@daily', 
    description='Group DAG with tasks',
    catchup=False) as dag:
    
    downloads = download_tasks()

    check_files = BashOperator(
        task_id='check_files',
        bash_command='echo "check_files" && sleep 10'
    )

    transforms = transform_tasks()

    downloads >> check_files >> transforms
