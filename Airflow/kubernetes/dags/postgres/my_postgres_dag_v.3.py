from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime
import logging

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id='my_postgres_dag_v.3', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['postgres'],
    catchup=False,
) as dag:

    task_0 = PostgresOperator(
        task_id='drop_a_pg_table',
        postgres_conn_id='postgres',
        sql='''
        DROP TABLE IF EXISTS my_test
        '''
    )
    
    task_1 = PostgresOperator(
        task_id='create_a_pg_table',
        postgres_conn_id='postgres',
        sql='''
        CREATE TABLE IF NOT EXISTS dag_trial (
        SN SERIAL PRIMARY KEY,
        REPORT_DATE DATE,
        USER_ID VARCHAR(30))
        '''
    )

    task_2 = PostgresOperator(
        task_id='data_insertion_n',
        postgres_conn_id='postgres',
        sql='''
        INSERT INTO dag_trial (REPORT_DATE, USER_ID)
        VALUES ('2023-10-12', 'NG2022')
        '''
    )

    logging.info(f'Drop table: {task_0.sql}')
    logging.info(f'Creating table: {task_1.sql}')
    logging.info(f'Inserting data: {task_2.sql}')
    
    task_0 >> task_1 >> task_2
