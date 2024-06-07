from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2023, 5, 1),
    'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def _test_task(execution_date):
    print(f"Execution month-day: {execution_date.month}-{execution_date.day}")
    if execution_date.day == 5:
        raise ValueError("Error on the 5th day of the month!")    

with DAG(
    dag_id='test_dag_v2.0',
    default_args=default_args,
    schedule_interval='@daily',
    dagrun_timeout=timedelta(seconds=60),
    catchup=True,
) as dag:

    task_a = BashOperator(
        owner='mark',
        task_id='task_a',
        bash_command='echo "Task A" && sleep 5',

    )

    task_b = BashOperator(
        owner='john',
        task_id='task_b',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, BashOperator from Airflow!" && echo "Try times: {{ ti.try_number }}" && exit 0',
    
    )

    task_c = PythonOperator(
        owner='mark',
        task_id='task_c',
        python_callable=_test_task,
        depends_on_past=True,

    )
    
    task_a >> task_b >> task_c
    