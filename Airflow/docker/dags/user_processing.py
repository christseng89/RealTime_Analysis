from airflow import DAG 
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG("user_processing", start_date=datetime(2023, 1, 1), schedule_interval="@daily", catchup=False) as dag:
    
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres",
        sql="""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            firstname VARCHAR NOT NULL,
            lastname VARCHAR NOT NULL,
            country VARCHAR NOT NULL,
            username VARCHAR NOT NULL,
            password VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            created_at TIMESTAMP NOT NULL
        );
        """
    )
    