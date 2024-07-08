from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file1 = Dataset('/tmp/my_file1.txt')

default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 5, 1),
    # 'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    # 'email_on_failure': True,
    # 'email_on_retry': False,
}

with DAG(
    dag_id='producer_v1consumer', 
    default_args=default_args,
    tags=['producer_consumer'],    
    schedule=[my_file1],
    catchup=False) as dag:

    @task #(inlets=[my_file]) # Define the task with the dataset as an inlet
    def read_dataset1():
        with open(my_file1.uri, 'r') as f:
            print(f.read())
            
    read_dataset1()
            