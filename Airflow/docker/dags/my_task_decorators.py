from airflow import DAG
from airflow.decorators import task
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 1),
    'retries': 1,
}

@task
def my_python_task():
    print("This is a Python task")

@task.branch
def my_branching_task():
    return "my_python_task"

@task.short_circuit
def my_short_circuit_task():
    return True

with DAG(
    dag_id='my_task_decorators',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    t1 = my_python_task()
    t2 = my_branching_task()
    t3 = my_short_circuit_task()

    t2 >> t3 >> t1
