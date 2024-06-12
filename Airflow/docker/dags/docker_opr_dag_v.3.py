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
}

@dag(
    dag_id='docker_opr_dag_v_3',
    description='Test DockerImage stock_image:1.0.0 with Mount',
    default_args=default_args,
    schedule_interval='@daily', 
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
        command='bash /tmp/output.sh',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        xcom_all=True,
        mounts=[Mount(source='/d/development/Real_Time_Analysis/Airflow/docker/stock_image/scripts', target='/tmp', type='bind')],
    )
    
    t1() >> t2

dag = docker_operator()
