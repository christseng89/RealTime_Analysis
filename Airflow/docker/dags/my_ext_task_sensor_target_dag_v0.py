from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

dag_id = "my_ext_task_sensor_target_v0"

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    external_task_sensor = ExternalTaskSensor(
        task_id='external_task_sensor',
        external_dag_id='my_ext_task_sensor_parent_v0',
        external_task_id='end',
        mode='poke',
        poke_interval=30,
        timeout=120,  # Increase timeout to 600 seconds
    
    )

    process_a = BashOperator(
        task_id='process_a',
        bash_command='echo "process_a"',
    )

    process_b = BashOperator(
        task_id='process_b',
        bash_command='echo "process_b"',
    )

    process_c = BashOperator(
        task_id='process_c',
        bash_command='echo "process_c"',
    )

    external_task_sensor >> process_a >> process_b >> process_c
