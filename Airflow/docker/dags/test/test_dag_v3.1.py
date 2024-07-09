from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.helpers import cross_downstream

from datetime import datetime, timedelta
import time

default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 5, 1),
    'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    # 'email_on_retry': False,
    # 'email_on_failure': True,

}

def _test_task(execution_date):
    print(f"Execution month-day: {execution_date.month}-{execution_date.day}")
    if execution_date.day == 35:
        raise ValueError("Error on the 35th day of the month!")    

def _test_sleep():
    print("Sleeping for 15 seconds...")
    time.sleep(15)
    
def sla_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(
        "The SLA missed callback arguments are: ",
        {
            "dag": dag,
            "task_list": task_list,
            "blocking_task_list": blocking_task_list,
            "slas": slas,
            "blocking_tis": blocking_tis,
        },
    )

# SLA - Service Level Agreement
with DAG(
    dag_id='test_dag_v3.1', # Test all_failed trigger_rule
    default_args=default_args,
    schedule_interval='*/15 1 * * *',
    dag_display_name="test_dag_v3.1 - SLA passed",
    tags=['test', 'sla'],
    catchup=False,
    sla_miss_callback=sla_callback, # SLA missed callback
) as dag:

    extract_a = PythonOperator(
        owner='mark',
        task_id='extract_a',
        python_callable=_test_sleep,
        wait_for_downstream=True,
        sla=timedelta(seconds=30) # Sleep for 15 seconds only

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
        bash_command='echo "Hi, BashOperator Process A!" && echo "Try times: {{ ti.try_number }}" && sleep 15',
        pool='process_tasks',
        priority_weight=2 # Lower priority than process_b - 2nd
    
    )

    process_b = BashOperator(
        owner='john',
        task_id='process_b',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, BashOperator Process B!" && echo "Try times: {{ ti.try_number }}" && sleep 15',
        pool='process_tasks',
        priority_weight=3 # Highest priority - 1st
        
    )

    process_c = BashOperator(
        owner='john',
        task_id='process_c',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, BashOperator Process C!" && echo "Try times: {{ ti.try_number }}" && sleep 15',
        pool='process_tasks',
        # priority_weight=1 # Lowest priority - 3rd, default = 1
        
    )

    clean_a = BashOperator(
        owner='john',
        task_id='clean_a',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, {{ti.task_id}}" && sleep 15',
        trigger_rule="all_failed"
        
    )

    clean_b = BashOperator(
        owner='john',
        task_id='clean_b',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, {{ti.task_id}}" && sleep 15',
        trigger_rule="all_failed"
        
    )
    
    clean_c = BashOperator(
        owner='john',
        task_id='clean_c',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, {{ti.task_id}}" && sleep 15',
        trigger_rule="all_failed"
        
    )
    
    store = PythonOperator(
        owner='mark',
        task_id='store',
        python_callable=_test_task,
        depends_on_past=True,

    )
    
    cross_downstream([extract_a, extract_b], [process_a, process_b, process_c])
    process_a >> clean_a
    process_b >> clean_b
    process_c >> clean_c
    [process_a, process_b, process_c] >> store    