from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    # 'schedule_interval': '@daily',
}

dag_id = "my_ext_task_sensor_parent_v0"

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule_interval='@daily',  # Change to '@daily
    catchup=False,
) as dag:

    start = BashOperator(
        task_id='start',
        bash_command='echo "Start"',
    )

    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Task 1"',
    )

    task2 = BashOperator(
        task_id='task2',
        bash_command='echo "Task 2"',
    )

    task3 = BashOperator(
        task_id='task3',
        bash_command='echo "Task 3"',
    )

    end = BashOperator(
        task_id='end',
        bash_command='echo "End"',
    )

    start >> task1 >> task2 >> task3 >> end
