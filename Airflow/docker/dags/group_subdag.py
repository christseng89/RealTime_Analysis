from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from subdags.subdag_downloads import subdag_downloads
from subdags.subdag_transforms import subdag_transforms
from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id='group_subdag', 
    default_args=default_args,
    schedule_interval='@daily', 
    description='Group DAG with subdags',
    catchup=False) as dag:
    args = {
        'start_date': default_args['start_date'],
        'schedule_interval': dag.schedule_interval,
        'catchup': dag.catchup
    }
    
    downloads = SubDagOperator(
        task_id='downloads',
        subdag=subdag_downloads(dag.dag_id, 'downloads', args)
    )

    check_files = BashOperator(
        task_id='check_files',
        bash_command='echo "check_files" && sleep 10'
    )

    transforms = SubDagOperator(
        task_id='transforms',
        subdag=subdag_transforms(dag.dag_id, 'transforms', args)
    )

    downloads >> check_files >> transforms
