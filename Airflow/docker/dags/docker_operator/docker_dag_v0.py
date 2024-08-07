from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'tags': ['docker', 'operator'],
}

dag = DAG(
    'docker_dag_v0',
    default_args=default_args,
    description='A simple DAG to run Docker commands',
    schedule_interval='@daily',
    tags=['docker'],
    catchup=False,
)

run_docker_command = BashOperator(
    task_id='run_docker_command',
    bash_command='docker run hello-world',
    dag=dag,
)

run_docker_version = BashOperator(
    task_id='run_docker_version',
    bash_command='docker --version',
    dag=dag,
)

run_docker_command >> run_docker_version
