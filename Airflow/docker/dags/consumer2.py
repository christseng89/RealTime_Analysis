from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file_1 = Dataset('/tmp/my_file_1.txt')
my_file_2 = Dataset('/tmp/my_file_2.txt')
default_args = {
    'owner': 'mark, john',
    'start_date': datetime(2024, 5, 1),
    'email': ['samfire5200@gmail.com', 'samfire5201@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG(
    dag_id='consumer2', 
    default_args=default_args,
    schedule=[my_file_1, my_file_2],
    catchup=False) as dag:

    @task #(inlets=[my_file_1]) # Define the task with the dataset as an inlet
    def read_dataset1():
        with open(my_file_1.uri, 'r') as f:
            print(f.read())

    @task #(inlets=[my_file_2]) # Define the task with the dataset as an inlet (Optional)
    def read_dataset2():
        with open(my_file_2.uri, 'r') as f:
            print(f.read())
                        
    read_dataset1() >> read_dataset2() # (Optional)
            