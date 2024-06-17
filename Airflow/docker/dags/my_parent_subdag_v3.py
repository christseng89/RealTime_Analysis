from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from subdags.my_parent_subdag_v2 import subdag_processes

from datetime import datetime

default_args = {
    'owner': 'mark, john, luke, matthew',
    'start_date': datetime(2024, 6, 5),
    'email': ['samfire5200@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'schedule_interval': '@daily',
}

dag_id = "my_parent_subdag_v3.0"

with DAG(
    dag_id=dag_id, 
    default_args=default_args,
    catchup=False,
) as dag:

    start = BashOperator(
        task_id='start',
        bash_command='echo "Start"',
    )

    group_process1 = SubDagOperator(
        task_id='group_process1',
        subdag=subdag_processes(
            dag_id,
            'group_process1',
            default_args,
            conf={'process_a': 1, 'process_b': 2, 'process_c': 3}
        ),
        mode='reschedule',
        timeout=60,
        propagate_skipped_state=False,
    )
    
    group_process2 = SubDagOperator(
        task_id='group_process2',
        subdag=subdag_processes(
            dag_id,
            'group_process2',
            default_args,
            conf={'process_a': 4, 'process_b': 6, 'process_c': 6}
        ),
        mode='reschedule',
        timeout=60,
        propagate_skipped_state=False,
    )

    group_process3 = SubDagOperator(
        task_id='group_process3',
        subdag=subdag_processes(
            dag_id,
            'group_process3',
            default_args,
            conf={'process_a': 7, 'process_b': 8, 'process_c': 9}
        ),
        mode='reschedule',
        timeout=60,
        propagate_skipped_state=False,
    )

    trigger_dag = TriggerDagRunOperator(
        task_id='trigger_dag',
        trigger_dag_id='my_parent_subdag_v2.0',
        conf={'process_a': 10, 'process_b': 11, 'process_c': 12},
        execution_date="{{ ds }}",
        reset_dag_run=True,
        wait_for_completion=True,
        poke_interval=60,
    )
                
    end = BashOperator(
        task_id='end',
        bash_command='echo "End"',
    )
    
    start >> [group_process1, group_process2, group_process3] >> trigger_dag >> end
