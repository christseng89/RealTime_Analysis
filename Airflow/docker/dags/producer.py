from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset('tmp/my_file.txt')

with DAG(
    dag_id='producer', 
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1), 
    catchup=False) as dag:
    
    @task(outlets=[my_file]) # Define the task with the dataset as an outlet
    def update_dataset():
        with open(my_file.uri, 'a+') as f:
            f.write('producer update')
    
    update_dataset()
    