from airflow import DAG

from airflow.operators.dummy import DummyOperator
from airflow.operators.datetime import BranchDateTimeOperator

from datetime import datetime, time

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}


with DAG(
    dag_id='my_branch_dt_dag_v.0', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['branch'],
    catchup=False,
) as dag:

    ml_training = DummyOperator(
        owner='luke',
        task_id='ml_training',
    )

    choose_branch = BranchDateTimeOperator(
        task_id='choose_branch',
        follow_task_ids_if_true=['process'],
        follow_task_ids_if_false=['notify_email', 'notify_slack'],
        # target_lower=datetime(2024, 6, 5, 12, 0, 0),
        # target_upper=datetime(2024, 6, 5, 18, 0, 0),
        target_lower=time(2, 30, 0),
        target_upper=time(23, 50, 0),
        use_task_execution_date=True,
    )
    
    process = DummyOperator(
        task_id='process',
    )
    
    notify_email = DummyOperator(
        task_id='notify_email',
    )
    
    notify_slack = DummyOperator(
        task_id='notify_slack',
    )
    
    ml_training >> choose_branch >> [ process, notify_email, notify_slack ]
    