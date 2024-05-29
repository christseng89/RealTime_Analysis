from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta

# Daily schedule
dag_daily = DAG(
    dag_id='daily_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

# Hourly schedule
dag_hourly = DAG(
    dag_id='hourly_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly',
    catchup=False
)

# Custom schedule using cron expression (every Monday at 7 AM)
dag_cron = DAG(
    dag_id='cron_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='0 7 * * 1',
    catchup=False
)

# Custom schedule using timedelta (every 3 days)
dag_timedelta = DAG(
    dag_id='timedelta_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=timedelta(days=3),
    catchup=False
)

# Tasks for each DAG
task1 = DummyOperator(task_id='task1', dag=dag_daily)
task2 = DummyOperator(task_id='task2', dag=dag_hourly)
task3 = DummyOperator(task_id='task3', dag=dag_cron)
task4 = DummyOperator(task_id='task4', dag=dag_timedelta)
