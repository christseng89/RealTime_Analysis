from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'docker_dag',
    default_args=default_args,
    description='A simple DAG to run Docker commands',
    schedule_interval='@daily',
    catchup=False,
)

run_docker_command = BashOperator(
    task_id='run_docker_command',
    bash_command='docker run hello-world',
    dag=dag,
)

run_docker_compose_command = BashOperator(
    task_id='run_docker_compose_command',
    bash_command='docker-compose up -d',
    dag=dag,
)

run_docker_command >> run_docker_compose_command
