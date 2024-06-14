from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.bash_operator import BashOperator
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

class CustomDockerOperator(DockerOperator):
    def pre_execute(self, context):
        self.command = "bash /tmp/scripts/output.sh"
        super().pre_execute(context)

@dag(
    dag_id='docker_opr_dag_v_3',
    description='Test DockerImage stock_image:1.0.0 with Mount',
    default_args=default_args,
    schedule_interval='@daily', 
    catchup=False,
)
def docker_operator_dag():
    
    @task()
    def t1():
        return 1

    t2 = CustomDockerOperator(
        task_id='docker_command',
        image='stock_image:1.0.0',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        xcom_all=True,
        mounts=[Mount(source='/d/development/Real_Time_Analysis/stock_image/scripts', target='/tmp/scripts', type='bind')],
    )
    
    run_docker_version = BashOperator(
        task_id='run_docker_version',
        bash_command='docker --version'
    )
    
    t1() >> t2 >> run_docker_version

dag = docker_operator_dag()
