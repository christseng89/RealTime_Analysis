from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,    
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'postgres_backup',
    default_args=default_args,
    tags=['postgres'],
    description='DAG to backup the PostgreSQL database',
    schedule_interval='@daily',
)

# Define the backup command, using current date for filename
backup_command = """
FILENAME=/opt/airflow/include/airflow_backup_{{ ds_nodash }}.sql
pg_dump -h airflow_postgres -p 5432 -U airflow airflow > $FILENAME
if [ $? -ne 0 ]; then
    echo "pg_dump failed"
    exit 1
else
    echo "Backup successful"
fi
"""

# Task to perform the backup
backup_task = BashOperator(
    task_id='backup_task',
    bash_command=backup_command,
    env={'PGPASSWORD': 'airflow'},
    dag=dag,
)

backup_end = DummyOperator(
    task_id='backup-end',
    dag=dag,
)

# Set task dependencies
backup_task >> backup_end
