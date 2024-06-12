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

### Pools

Airflow UI => Admin => Pools => + Add a new record

- Pool (process_tasks)
- Slots (1)
- Description (Pool to run Process Tasks sequentially - test_dag_v2.1.py)
=> Save

airflow pools list
    pool          | slots | description
    ==============+=======+==========================================================
    default_pool  | 128   | Default pool
    process_tasks | 1     | Pool to run Process Tasks sequentially - test_dag_v2.1.py

### Docker Compose (WSL2)

curl -LfO <https://airflow.apache.org/docs/apache-airflow/2.4.2/docker-compose.yaml>

### Variables

docker exec airflow_scheduler airflow variables list

    key
    ----------------
    path
    filename
    my_settings
    api_key_aws
    password_postgres

### Backup Airflow Database

<https://medium.com/@fninsiima/de-mini-series-part-two-57770ff7cdf9>

// Same practices could be applied for Microservices databases.

### Postgres Backup and Restore

// Backup
pg_dump -U airflow -d airflow > airflow.sql

// Restore (Not tested)
dropdb -U airflow airflow
createdb -U airflow airflow

psql -U airflow -d airflow -f airflow.sql

// Backup to local machine
docker exec airflow_postgres pg_dump -U airflow -d airflow > airflow.sql

// Restore from local machine (Not tested)
docker exec dropdb -U airflow airflow
docker exec createdb -U airflow airflow
docker exec psql -U airflow -d airflow -f airflow.sql
