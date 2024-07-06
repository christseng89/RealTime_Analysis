from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime
import os

my_file_1 = Dataset('/tmp/my_file_1.txt')
my_file_2 = Dataset('/tmp/my_file_2.txt')

with DAG(
    dag_id='producer2', 
    schedule_interval='@daily',
    tags=['producer_consumer'],
    start_date=datetime(2023, 1, 1), 
    catchup=False
) as dag:
    
    @task(outlets=[my_file_1])  # Define the task with the dataset as an outlet
    def update_dataset1():
        # Ensure the directory exists
        os.makedirs(os.path.dirname(my_file_1.uri), exist_ok=True)
        
        # Open the file and write the update
        with open(my_file_1.uri, 'a+') as f:
            f.write('producer update 1\n')
    
    @task(outlets=[my_file_2])  # Define the task with the dataset as an outlet
    def update_dataset2():
        # Ensure the directory exists
        os.makedirs(os.path.dirname(my_file_2.uri), exist_ok=True)
        
        # Open the file and write the update
        with open(my_file_2.uri, 'a+') as f:
            f.write('producer update 2\n')
    
    update_dataset1() >> update_dataset2()
