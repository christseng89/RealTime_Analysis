from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator

def download_tasks():
    with TaskGroup('downloads', tooltip="Download tasks") as downloads:
        
        download_a = BashOperator(
            task_id='download_a',
            bash_command='sleep 5'
        )

        download_b = BashOperator(
            task_id='download_b',
            bash_command='sleep 5'
        )

        download_c = BashOperator(
            task_id='download_c',
            bash_command='sleep 5'
        )

    return downloads