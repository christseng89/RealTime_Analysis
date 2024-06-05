from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john',
}

def _test_task(**context):
    print(context)
    print("DS: " + context['ds'])
    print("DAG ID: " + context['dag'].dag_id)
    print("DAG Run ID: " + context['dag_run'].run_id)
    print("Task ID: " + context['task_instance'].task_id)

with DAG(
    dag_id='test_dag_v0',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    test_task1 = PythonOperator(
        owner='mark',
        task_id='test_task_v01',
        python_callable=_test_task,

    )

    test_task2 = PythonOperator(
        owner='john',
        task_id='test_task_v02',
        python_callable=_test_task,

    )

    test_task1 >> test_task2
    