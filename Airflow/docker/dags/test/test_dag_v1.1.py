from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2023, 1, 1),
    'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def _test_task(**context):
    # print(context)
    # print("DS: " + context['ds'])
    # print("DAG ID: " + context['dag'].dag_id)
    # print("DAG Run ID: " + context['dag_run'].run_id)
    print("Task ID: " + context['task_instance'].task_id)

with DAG(
    dag_id='test_dag_v1.1',
    # start_date=days_ago(2), 
    ## Although days_ago() it is working, but not recommended...
    # start_date=datetime(2023, 1, 1), 
    ## change the start_date to default_args
    # dag_display_name='test_dag_v1.1 with exit 1',
    default_args=default_args,
    schedule_interval='@daily',
    tags=['test'],
    catchup=False,
) as dag:

    # Generate dynamic task IDs
    
    for i in range(6):
        task_id = f'test_task_{i}'
        test_task = PythonOperator(
            task_id=task_id,
            python_callable=_test_task,
        )
        
        if i == 0:
            test_task_0 = test_task
        if i == 1:
            test_task_1 = test_task
        if i == 2:
            test_task_2 = test_task
        if i == 3:
            test_task_3 = test_task    
        if i == 4:
            test_task_4 = test_task           
        if i == 5:
            test_task_5 = test_task                           
        # Assign test_task_1 variable

    test_task_bash = BashOperator(
        task_id='test_task_bach',
        retries=3,
        retry_delay=timedelta(seconds=5),
        retry_exponential_backoff=True, # Useful for API calls
        bash_command='echo "Hi, BashOperator from Airflow!" && echo "Try times: {{ ti.try_number }}" && sleep 5 && exit 1',
        # https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/taskinstance/index.html
    )
    
    test_task_0 >> [test_task_1, test_task_2] >> test_task_5>> [test_task_3, test_task_4] >> test_task_bash