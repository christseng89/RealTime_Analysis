from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset('tmp/my_file.txt')

with DAG(
    dag_id='consumer', 
    start_date=datetime(2023, 1, 1), 
    schedule=[my_file],
    catchup=False) as dag:

    @task #(inlets=[my_file]) # Define the task with the dataset as an inlet
    def read_dataset():
        with open(my_file.uri, 'r') as f:
            print(f.read())
            
    read_dataset()
            