from airflow import DAG
from airflow.operators.bash import BashOperator
 
from datetime import datetime
 
with DAG(
    dag_id='my_parallel_dag', 
    start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', 
    dag_display_name='my_parallel_dag w high_cpu queue',
    tags=['test', 'parallel'],
    catchup=False) as dag:
 
    extract_a = BashOperator(
        task_id='extract_a',
        bash_command='sleep 5'
    )
 
    extract_b = BashOperator(
        task_id='extract_b',
        bash_command='sleep 5'
    )
 
    load_a = BashOperator(
        task_id='load_a',
        bash_command='sleep 5'
    )
 
    load_b = BashOperator(
        task_id='load_b',
        bash_command='sleep 5'
    )
 
    transform = BashOperator(
        task_id='transform',
        # queue='high_cpu', # Not working in k8s
        bash_command='sleep 5'
    )
 
    extract_a >> load_a
    extract_b >> load_b
    [load_a, load_b] >> transform
    