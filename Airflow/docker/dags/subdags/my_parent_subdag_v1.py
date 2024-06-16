from airflow import DAG
from airflow.operators.bash import BashOperator

def subdag_processes(
    parent_dag_id, 
    child_dag_id, 
    default_args
):

    with DAG(
        dag_id=f'{parent_dag_id}.{child_dag_id}',
        default_args=default_args,
    ) as dag:
        
        process_a = BashOperator(
            task_id='process_a',
            bash_command='echo "Process A"',
        )
    
        process_b = BashOperator(
            task_id='process_b',
            bash_command='echo "Process B"',
        )
        
        process_c = BashOperator(
            task_id='process_c',
            bash_command='echo "Process C"',
        )
    
    return dag        