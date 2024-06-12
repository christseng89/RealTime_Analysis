from airflow import DAG
from airflow.decorators import task, dag
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

@dag(
    dag_id='docker_opr_dag_v_1',
    description='Test Docker Operator',
    default_args=default_args,
    schedule_interval='@daily', 
    catchup=False,
)
def docker_operator_dag_v_1():
    
    @task()
    def t1():
        return 1

    t2 = DockerOperator(
        task_id='docker_command',
        image='alpine:latest',
        api_version='auto',
        auto_remove=True,
        command='echo "Hello, World!"',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
    )
    
    t1() >> t2

dag = docker_operator_dag_v_1()
