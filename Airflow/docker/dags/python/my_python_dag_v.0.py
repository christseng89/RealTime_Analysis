from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from datetime import datetime, timedelta

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

# def _task_a(path, filename, ti, execution_date):
def _task_a(ti, execution_date, path, filename):
    print(f"Path: {path}, Filename: {filename}")
    print(f"Execution month-day: {execution_date.month}-{execution_date.day}, Task Id: {ti.task_id}")
    
with DAG(
    dag_id='my_python_dag_v.0', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['python'],
    catchup=False,
) as dag:
 
    task_a = PythonOperator(
        owner='luke',
        task_id='task_a',
        python_callable=_task_a,
        provide_context=True,
        # op_args=['/usr/local/airflow/data','my_data.csv'],
        # op_kwargs={'path': '/usr/local/airflow/data', 'filename': 'my_data.csv'},
        # op_kwargs={'path': '{{var.value.path}}', 'filename': '{{var.value.filename}}'},
        op_kwargs=Variable.get('my_settings', deserialize_json=True),
    )
    