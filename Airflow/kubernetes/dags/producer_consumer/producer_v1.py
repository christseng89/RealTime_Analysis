from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime
import os

my_file1 = Dataset('/tmp/my_file1.txt')
my_file2 = Dataset('/tmp/my_file2.txt')

with DAG(
    dag_id='producer_v1', 
    schedule_interval='@daily',
    tags=['producer_consumer'],
    start_date=datetime(2023, 1, 1), 
    catchup=False) as dag:
    
    @task(outlets=[my_file1])  # Define the task with the dataset as an outlet
    def update_dataset1():
        # Ensure the directory exists
        os.makedirs(os.path.dirname(my_file1.uri), exist_ok=True)
        
        # Open the file and write the update
        with open(my_file1.uri, 'a+') as f:
            f.write('producer update 1\n')
    
    @task(outlets=[my_file2])  # Define the task with the dataset as an outlet
    def update_dataset2():
        # Ensure the directory exists
        os.makedirs(os.path.dirname(my_file2.uri), exist_ok=True)
        
        # Open the file and write the update
        with open(my_file2.uri, 'a+') as f:
            f.write('producer update 1\n')    
            
    update_dataset1() >> update_dataset2()
