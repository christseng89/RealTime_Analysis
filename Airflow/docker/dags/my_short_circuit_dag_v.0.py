from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import ShortCircuitOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    # 'schedule_interval': '@daily',
}

dag_id = "my_short_circuit_dag_v0"

def _is_monday(execution_date, **context):
    print(f"Execution date: {execution_date.strftime('%A')}")
    return execution_date.strftime('%A') == 'Monday'

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

    is_monday = ShortCircuitOperator(
        task_id='is_monday',
        python_callable=_is_monday,
        # python_callable=lambda: datetime.now().isoweekday() in [1, 2],
    )
    
    task3 = BashOperator(
        task_id='task3',
        bash_command='echo "Task 3"',
    )


    start >> task1 >> task2 >> is_monday >> task3 
