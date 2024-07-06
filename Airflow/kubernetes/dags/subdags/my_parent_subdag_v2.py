from airflow import DAG
from airflow.operators.bash import BashOperator

def subdag_processes(
    parent_dag_id, 
    child_dag_id, 
    default_args,
    conf
):
    default_args['pool'] = 'process_tasks'  # 1 process at a time
    with DAG(
        dag_id=f'{parent_dag_id}.{child_dag_id}',
        default_args=default_args,
    ) as dag:
        
        task_process_a = BashOperator(
            task_id='process_a',
            bash_command=f'echo "Process A" && echo {conf["process_a"]}',
        )
    
        task_process_b = BashOperator(
            task_id='process_b',
            bash_command=f'echo "Process B" && echo {conf["process_b"]}',
        )
        
        task_process_c = BashOperator(
            task_id='process_c',
            bash_command=f'echo "Process C" && echo {conf["process_c"]}',
        )
        
        # task_process_a >> task_process_b >> task_process_c
    
    return dag
