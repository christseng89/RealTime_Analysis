from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

@task(task_id='task_a')
def task_a(**kwargs):
    params = kwargs['params']
    path = params['path']
    filename = params['filename']
    logical_date = kwargs['logical_date']
    ti = kwargs['ti']
    print(f"Path: {path}, Filename: {filename}")
    print(f"Logical date's month-day: {logical_date.month}-{logical_date.day}, Task Id: {ti.task_id}")

with DAG(
    dag_id='my_python_dag_v_1', 
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    
) as dag:
    
    store = BashOperator(
        owner='mark',
        task_id='store',
        bash_command='echo "Store data"',
    )
    
    settings = Variable.get('my_settings', deserialize_json=True)
    task_a(params=settings) >> store
