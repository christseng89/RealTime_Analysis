from airflow import DAG

from airflow.operators.dummy import DummyOperator
from airflow.operators.sql import BranchSQLOperator

from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime
import yaml
import os

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}


with DAG(
    dag_id='my_branch_sql_dag_v.1', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['branch'],
    catchup=False,
) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='sql/create_table_partners.sql',
    )

    insert_records = PostgresOperator(
        task_id='insert_records',
        postgres_conn_id='postgres',
        sql='sql/insert_records_partners_v1.sql',
    )
    
    choose_branch = BranchSQLOperator(
        task_id='choose_branch',
        conn_id='postgres',
        sql='sql/choose_branch_partners.sql',
        follow_task_ids_if_true=['process'],
        follow_task_ids_if_false=['notify_email', 'notify_slack'],
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
    
    create_table >> insert_records >> choose_branch >> [ process, notify_email, notify_slack ]
    