from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.helpers import cross_downstream
from airflow.exceptions import AirflowTaskTimeout

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
    if execution_date.day == 35:
        raise ValueError("Error on the 35th day of the month!")    

def _extract_on_success(context):
        print(f"Task id: {context['task_instance'].task_id} is successful!")
    
def _extract_on_failure(context):
     if (isinstance(context['exception'], AirflowTaskTimeout)): 
        print(f"Task id: {context['task_instance'].task_id} TIMEOUT with Exception Error {context['exception']}!")
     else:
        print(f"Task id: {context['task_instance'].task_id} is failed with another Exception Error {context['exception']}!")
           
with DAG(
    dag_id='test_dag_v2.4.1', # Test all_failed trigger_rule
    default_args=default_args,
    schedule_interval='@daily',
    # dagrun_timeout=timedelta(seconds=60),
    dag_display_name='test_dag_v2.4.1 with timeout and all_failed',
    tags=['test'],
    catchup=False,
) as dag:

    extract_a = BashOperator(
        owner='mark',
        task_id='extract_a',
        bash_command='echo "Task A Timeout" && sleep 15',
        wait_for_downstream=True,
        execution_timeout=timedelta(seconds=10), # Timeout for the task
        on_success_callback=_extract_on_success,
        on_failure_callback=_extract_on_failure,

    )
    
    extract_b = BashOperator(
        owner='mark',
        task_id='extract_b',
        bash_command='echo "Task B Timeout" && sleep 15',
        wait_for_downstream=True,
        execution_timeout=timedelta(seconds=10), # Timeout for the task
        on_success_callback=_extract_on_success,
        on_failure_callback=_extract_on_failure,
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
        trigger_rule="all_failed",
        
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