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

### Delete the volume between runs

docker-compose --profile flower down -v

 ✔ Volume docker_postgres-db-volume  Removed

docker-compose --profile flower up -d

[+] Running 12/12
 ✔ Network docker_default              Created
 ✔ Volume "docker_postgres-db-volume"  Created ***
 ✔ Container airflow_elastic           Started
 ...

### Connection List

airflow connections list

id | conn_id          | conn_type | description  | host                   | login   | password | port
===+================  +=========  +==============+========================+=========+========= +======
1  | postgres         | postgres  | Postgres     | postgres               | airflow | airflow  | 5432
2  | elastic_default  | http      | Elastic      | elastic                |         | None     | 9200
3  | user_api         | http      | User API     | https://randomuser.me/ |         | None     | None
