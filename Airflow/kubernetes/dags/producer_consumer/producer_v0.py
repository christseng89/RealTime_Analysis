from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime
import os

my_file = Dataset('/tmp/my_file.txt')

with DAG(
    dag_id='producer_v0', 
    schedule_interval='@daily',
    tags=['producer_consumer'],
    start_date=datetime(2023, 1, 1), 
    catchup=False) as dag:
    
    @task(outlets=[my_file])  # Define the task with the dataset as an outlet
    def update_dataset():
        # Ensure the directory exists
        os.makedirs(os.path.dirname(my_file.uri), exist_ok=True)
        
        # Open the file and write the update
        with open(my_file.uri, 'a+') as f:
            f.write('producer update\n')
    
    update_dataset()
