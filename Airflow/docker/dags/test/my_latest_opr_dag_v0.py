from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.latest_only import LatestOnlyOperator

from airflow.utils.dates import days_ago

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': days_ago(3),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    # 'schedule_interval': '@daily',
}

dag_id = "my_latest_opr_dag_v0"

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    tags=['test', 'latest_only_operator'],
    schedule_interval='@daily',  # Change to '@daily
    catchup=True,
) as dag:

    start = BashOperator(
        task_id='start',
        bash_command='echo "Start"',
    )

    getting_data = BashOperator(
        task_id='getting_data',
        bash_command='echo "getting_data"',
    )

    create_email = BashOperator(
        task_id='create_email',
        bash_command='echo "create_email"',
    )

    is_latest = LatestOnlyOperator(
        task_id='is_latest',
    )
    
    sending_email = BashOperator(
        task_id='sending_email',
        bash_command='echo "sending_email"',
    )

    start >> getting_data >>  create_email >> is_latest >> sending_email
