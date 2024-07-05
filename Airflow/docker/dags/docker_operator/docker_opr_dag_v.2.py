from airflow import DAG
from airflow.decorators import task, dag
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from docker.types import Mount

default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'tags': ['docker', 'operator'],
}

@dag(
    dag_id='docker_opr_dag_v_2',
    description='Test DockerImage stock_image:1.0.0',
    default_args=default_args,
    dag_display_name='docker_opr_dag_v_2-stock_image',
    schedule_interval='@daily', 
    tags=['docker'],
    catchup=False,
)
def docker_operator():
    
    @task()
    def t1():
        return 1

    t2 = DockerOperator(
        task_id='docker_command',
        image='stock_image:1.0.0',
        api_version='auto',
        auto_remove=True,
        command='python3 stock_data.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        xcom_all=True,
        retrieve_output=True,
        retrieve_output_path='/tmp/script.out',
        
    )
    
    t1() >> t2

dag = docker_operator()
