from airflow import DAG
from airflow.operators.python import PythonOperator

from pprint import pprint
from datetime import datetime

def _test_task(**context):
    pprint(context)
    print("DS: " + context['ds'])
    print("DAG Run ID: " + context['dag_run'].run_id)
    print("Execution date: " + context['execution_date'])
    print("Task instance key: " + context['task_instance_key_str'])
    print("Task instance try number: " + context['task_instance_try_number'])
    print("Task instance id: " + context['task_instance_id'])
    print("Task instance object: " + context['task_instance_object'])
    print("Task instance state: " + context['task_instance_state'])
    print("Task instance task id: " + context['task_instance_task_id'])
    print("Task instance dag id: " + context['task_instance_dag_id'])
    print("Task instance execution date: " + context['task_instance_execution_date'])

with DAG(
    dag_id='test_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    test_task = PythonOperator(
        task_id='test_task',
        python_callable=_test_task,
    )
