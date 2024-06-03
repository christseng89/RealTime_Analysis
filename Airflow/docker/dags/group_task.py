from airflow import DAG
from airflow.operators.bash import BashOperator

from groups.group_downloads import download_tasks
from groups.group_transforms import transform_tasks

from datetime import datetime

with DAG(
    dag_id='group_task', 
    start_date=datetime(2023, 1, 1), 
    schedule_interval='@daily', 
    description='Group DAG with tasks',
    catchup=False) as dag:
    
    downloads = download_tasks()

    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )

    transforms = transform_tasks()

    downloads >> check_files >> transforms
