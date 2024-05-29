from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

custom_timetable = CustomHolidayTimetable()

with DAG(
    dag_id='custom_holiday_timetable_dag',
    start_date=datetime(2023, 1, 1),
    timetable=custom_timetable,
    catchup=False,
) as dag:
    start = DummyOperator(task_id='start')
