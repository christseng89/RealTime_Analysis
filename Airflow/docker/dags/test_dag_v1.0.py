from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

def _test_task(**context):
    # print(context)
    # print("DS: " + context['ds'])
    # print("DAG ID: " + context['dag'].dag_id)
    # print("DAG Run ID: " + context['dag_run'].run_id)
    print("Task ID: " + context['task_instance'].task_id)

with DAG(
    dag_id='test_dag_v1.0',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Generate dynamic task IDs
    test_task_1 = None  # Define test_task_1 variable
    
    for i in range(4):
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
        # Assign test_task_1 variable

    test_task_0 >> [test_task_1, test_task_2] >> test_task_3