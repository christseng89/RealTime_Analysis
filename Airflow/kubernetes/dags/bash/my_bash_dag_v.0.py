from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 6, 1),
    # 'email': ['samfire5200@gmail.com'],
    # 'email_on_failure': True,
    # 'email_on_retry': False,
    # 'tags': ['bash', 'operator'],
}

with DAG(
    dag_id='my_bash_dag_v_0', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['bash'],
    catchup=False,
    
) as dag:
    
    execute_command = BashOperator(
        owner='mark',
        task_id='execute_command',
        bash_command='scripts/test_script1.sh',
        do_xcom_push=False,
        env={'aws_key': '{{var.value.api_key_aws}}'},
        skip_exit_code=10,
    )
