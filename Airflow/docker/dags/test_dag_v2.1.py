from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.helpers import cross_downstream

from datetime import datetime, timedelta

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 5, 1),
    'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def _test_task(execution_date):
    print(f"Execution month-day: {execution_date.month}-{execution_date.day}")
    if execution_date.day == 5:
        raise ValueError("Error on the 32th day of the month!")    

with DAG(
    dag_id='test_dag_v2.1',
    default_args=default_args,
    schedule_interval='@daily',
    # dagrun_timeout=timedelta(seconds=60),
    catchup=False,
) as dag:

    extract_a = BashOperator(
        owner='mark',
        task_id='extract_a',
        bash_command='echo "Task A" && sleep 5',
        wait_for_downstream=True,

    )
    
    extract_b = BashOperator(
        owner='mark',
        task_id='extract_b',
        bash_command='echo "Task A" && sleep 5',
        wait_for_downstream=True,

    )

    process_a = BashOperator(
        owner='john',
        task_id='process_a',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, BashOperator from Airflow!" && echo "Try times: {{ ti.try_number }}" && sleep 15',
        pool='process_tasks'
    
    )

    process_b = BashOperator(
        owner='john',
        task_id='process_b',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, BashOperator from Airflow!" && echo "Try times: {{ ti.try_number }}" && sleep 15',
        pool='process_tasks'
        
    )

    process_c = BashOperator(
        owner='john',
        task_id='process_c',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, BashOperator from Airflow!" && echo "Try times: {{ ti.try_number }}" && sleep 15',
        pool='process_tasks'
        
    )


    store = PythonOperator(
        owner='mark',
        task_id='store',
        python_callable=_test_task,
        depends_on_past=True,

    )
    
    cross_downstream([extract_a, extract_b], [process_a, process_b, process_c])
    [process_a, process_b, process_c] >> store
    