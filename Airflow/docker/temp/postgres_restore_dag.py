from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'postgres_restore',
    default_args=default_args,
    tags=['postgres'],
    description='DAG to restore the PostgreSQL database from backup',
    schedule_interval="@daily",
)

# Define the restore command
restore_command = """
FILENAME=/opt/airflow/includes/airflow_backup_{{ ds_nodash }}.sql
psql -h airflow_postgres -p 5432 -U airflow -d airflow -v ON_ERROR_STOP=0 -f $FILENAME
if [ $? -ne 0 ]; then
    echo "psql restore failed"
    exit 1
else
    echo "Restore successful"
fi
"""

# Task to perform the restore
restore_task = BashOperator(
    task_id='restore_task',
    bash_command=restore_command,
    env={'PGPASSWORD': 'airflow'},
    dag=dag,
)

restore_end = DummyOperator(
    task_id='restore-end',
    dag=dag,
)

# Set task dependencies
restore_task >> restore_end
