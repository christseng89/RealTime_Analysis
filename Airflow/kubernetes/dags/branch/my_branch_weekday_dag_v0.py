from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.weekday import BranchDayOfWeekOperator
from airflow.utils.weekday import WeekDay

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id='my_branch_weekday_dag_v0', 
    default_args=default_args,
    dag_display_name="my_branch_weekday_dag_v0 w email on failure",
    schedule_interval='@daily',
    tags=['branch'],
    catchup=True,
) as dag:

    ml_training = DummyOperator(
        owner='luke',
        task_id='ml_training',
    )

    choose_branch = BranchDayOfWeekOperator(
        task_id='choose_branch',
        week_day={WeekDay.MONDAY, WeekDay.WEDNESDAY, WeekDay.FRIDAY},
        follow_task_ids_if_true='process',
        follow_task_ids_if_false=['notify_email', 'notify_slack'],
        use_task_execution_day=True,
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
    
    ml_training >> choose_branch >> [process, notify_email, notify_slack]
