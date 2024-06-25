from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from airflow.models import Variable

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

def _python_a(ti, execution_date, path, filename):
    print(f"Path: {path}, Filename: {filename}")
    print(f"Execution month-day: {execution_date.month}-{execution_date.day}, Task Id: {ti.task_id}")
    
with DAG(
    dag_id='my_postgres_dag_v.0', 
    default_args=default_args,
    schedule_interval='@daily',
    tags=['postgres'],
    catchup=False,
) as dag:

    python_a = PythonOperator(
        owner='luke',
        task_id='python_a',
        python_callable=_python_a,
        provide_context=True,
        op_kwargs=Variable.get('my_settings', deserialize_json=True),
    )

    postgres_create_table = PostgresOperator(
        task_id='postgres_create_table',
        postgres_conn_id='postgres',
        sql="sql/create_table_my_table.sql"
    )
    
    postgres_insert_record = PostgresOperator(
        task_id='postgres_insert_record',
        postgres_conn_id='postgres',
        sql="sql/insert_record_my_table.sql"
    )

    postgres_query = PostgresOperator(
        task_id='postgres_query',
        postgres_conn_id='postgres',
        # sql="sql/query_my_table.sql",
        sql=[
        "SELECT value FROM my_table where id = 1",    
        "sql/query_my_table.sql",
        ],
    )
        
    python_a >> postgres_create_table >> postgres_insert_record >> postgres_query
