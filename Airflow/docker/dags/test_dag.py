from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

def _test_task(**context):
    print(context)
    print("DS: " + context['ds'])
    print("DAG ID: " + context['dag'].dag_id)
    print("DAG Run ID: " + context['dag_run'].run_id)

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
