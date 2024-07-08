from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator

def transform_tasks():
    with TaskGroup('transforms', tooltip="Transform tasks") as transforms:

        transform_a = BashOperator(
            task_id='transform_a',
            bash_command='sleep 5'
        )

        transform_b = BashOperator(
            task_id='transform_b',
            bash_command='sleep 5'
        )

        transform_c = BashOperator(
            task_id='transform_c',
            bash_command='sleep 5'
        )

    return transforms