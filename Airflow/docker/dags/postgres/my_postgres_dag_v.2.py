from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable

from datetime import datetime

postgres_conn_id = 'postgres'

class CustomPostgresOperator(PostgresOperator):
    template_fields = ('sql', 'parameters')

    def __init__(self, *args, **kwargs):
        super(CustomPostgresOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        hook = PostgresHook(postgres_conn_id=postgres_conn_id)
        self.log.info('Executing: %s', self.sql)
        result = hook.get_first(self.sql, parameters=self.parameters)
        if result:
            self.log.info("Query Result: %s", result)
            context['ti'].xcom_push(key='query_result', value=result[0])
        return result

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
    return "Python A Task Completed"

with DAG(
    dag_id='my_postgres_dag_v.2', 
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
        postgres_conn_id=postgres_conn_id,
        sql="sql/create_table_my_table.sql"
    )
    
    postgres_insert_record = CustomPostgresOperator(
        task_id='postgres_insert_record',
        postgres_conn_id=postgres_conn_id,
        sql="sql/insert_record_my_table_v1.sql",
        parameters={"id": 1, "value": "{{ ti.xcom_pull(task_ids='python_a') }}"}
    )

    postgres_query_all = PostgresOperator(
        task_id='postgres_query_all',
        postgres_conn_id=postgres_conn_id,
        sql=[
        "sql/query_by_id_my_table.sql",   
        "sql/query_my_table.sql",
        ],
    )

    postgres_query_by_id = CustomPostgresOperator(
        task_id='postgres_query_by_id',
        postgres_conn_id=postgres_conn_id,
        sql="sql/query_by_id_my_table.sql",
    )
        
    python_a >> postgres_create_table >> postgres_insert_record >> postgres_query_all >> postgres_query_by_id 
