from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator

def task_group_process(group_id, conf):
    with TaskGroup(
        group_id=group_id,
    ) as task_group_process:
        
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
        
        with TaskGroup(
            group_id=f'{group_id}_publish',          
        ) as tasks_group_publish:
            
            task_publish_a = BashOperator(
                task_id='publish_a',
                bash_command=f'echo "Publish A" && echo {conf["publish_a"]}',
            )
            
            task_publish_b = BashOperator(
                task_id='publish_b',
                bash_command=f'echo "Publish B" && echo {conf["publish_b"]}',
            )
            
            task_publish_c = BashOperator(
                task_id='publish_c',
                bash_command=f'echo "Publish C" && echo {conf["publish_c"]}',
            )
            
            task_publish_a >> task_publish_b >> task_publish_c
        
        task_process_a >> task_process_b >> task_process_c >> tasks_group_publish
    
    return task_group_process
