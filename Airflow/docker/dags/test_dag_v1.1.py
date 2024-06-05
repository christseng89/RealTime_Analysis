from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2023, 1, 1),
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
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Generate dynamic task IDs
    test_task_1 = None  # Define test_task_1 variable
    
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

    test_task_0 >> [test_task_1, test_task_2] >> test_task_5>> [test_task_3, test_task_4] 