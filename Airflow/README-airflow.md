# Access Airflow Containers

## Access PostgreSQL

docker exec -it airflow_postgres /bin/bash
    psql -U airflow -d airflow
        select * from dag;
        select * from dag_run;
        select * from task_instance;
        \q
    exit

## Access Airflow Scheduler

docker exec -it airflow_scheduler /bin/bash
    airflow dags list

## Rename DAG

docker exec -it airflow_scheduler /bin/bash
    airflow dags list
    airflow dags pause <DAG_ID>
    airflow dags unpause <DAG_ID>
    airflow dags delete <DAG_ID>
    airflow dags list

// from logs folder delete all files with the name likes the [original DAG_ID]

### User

airflow users create --username mark --password mark --firstname Mark --lastname User --role User --email mark@example.com
