# Apache Airflow

## DAG (Directed Acyclic Graph)

DAG (Directed Acyclic Graph) is a core concept representing a workflow. A DAG is a collection of tasks organized in a way that explicitly defines their dependencies and execution order. Here are some key aspects of DAGs in Airflow.

- Directed: The workflow has a clear direction, where each task points to its subsequent tasks.
  有向：工作流有明确的方向，每个任务指向其后续任务。
- Acyclic: There are no cycles or loops in the graph, ensuring that the tasks do not re-execute infinitely.
  无环：图中没有循环或环，确保任务不会无限循环地重新执行。

## Operators

An Operator is a fundamental building block of a workflow, representing a single task in a DAG (Directed Acyclic Graph). Operators define what kind of task is executed, whether it be running a shell command, executing Python code, transferring data between systems, or any other unit of work.

Operators are atomic units of execution within a DAG. (运算符是DAG中的原子执行单元。)

### Types of Operators

- Action Operators:
  - BashOperator
  - PythonOperator
- Transfer Operators:
  - S3ToRedshiftTransfer: Transfers data from Amazon S3 to Amazon Redshift.
  - MySqlToGoogleCloudStorageOperator: Transfers data from MySQL to Google Cloud Storage.
- Sensor Operators: Wait for a condition to be met before proceeding.
  - TimeSensor: Waits until a specific time.
  - S3KeySensor: Waits for a file to appear in an S3 bucket.

### Operator Summary

- Operators: Core components in Airflow DAGs that define the tasks to be performed.
- Types: Include Action Operators, Transfer Operators, Sensor Operators, DummyOperator, SubDagOperator, and other specific operators.
- Custom Operators: Can be created to handle specific needs not covered by built-in operators, providing flexibility to extend Airflow's capabilities.

### Installing Apache Airflow - via Terminal (Admin)

D: && cd D:\development\Real_Time_Analysis\Airflow\docker
docker-compose up -d

- airflow-webserver Pulling
- redis [⣿⣿⣿⣶⠀⠀] Pulling
- airflow-init Pulling
- airflow-scheduler Pulling
- postgres [⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿⣿]  65.4MB / 149MB   Pulling
- airflow-worker Pulling
- airflow-triggerer [⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿] 230.8MB / 323.5MB Pulling
  
[+] Running 8/8
 ✔ Network docker_default                Created                                                                   0.0s
 ✔ Container docker-postgres-1           Healthy                                                                   6.6s
 ✔ Container docker-redis-1              Healthy                                                                   6.6s
 ✔ Container docker-airflow-init-1       Exited                                                                   24.1s
 ✔ Container docker-airflow-webserver-1  Started                                                                  24.3s
 ✔ Container docker-airflow-scheduler-1  Started                                                                  24.2s
 ✔ Container docker-airflow-triggerer-1  Started                                                                  24.3s
 ✔ Container docker-airflow-worker-1     Started                                                                  24.3s

docker-compose ps

NAME                         IMAGE                  COMMAND                  SERVICE             STATUS               PORTS
docker-airflow-scheduler-1   apache/airflow:2.4.2   "/usr/bin/dumb-init …"   airflow-scheduler   (healthy)            8080/tcp
docker-airflow-triggerer-1   apache/airflow:2.4.2   "/usr/bin/dumb-init …"   airflow-triggerer   (healthy)            8080/tcp
docker-airflow-webserver-1   apache/airflow:2.4.2   "/usr/bin/dumb-init …"   airflow-webserver   (health: starting)   0.0.0.0:8080->8080/tcp
docker-airflow-worker-1      apache/airflow:2.4.2   "/usr/bin/dumb-init …"   airflow-worker      (health: starting)   8080/tcp
docker-postgres-1            postgres:13            "docker-entrypoint.s…"   postgres            (healthy)            5432/tcp
docker-redis-1               redis:latest           "docker-entrypoint.s…"   redis               (healthy)            6379/tcp

<http://localhost:8080>

airflow/airflow

### Airflow Summary

- Airflow is an orchestrator, not a processing framework. Process your gigabytes of data outside of Airflow
  (i.e. You have a Spark cluster, you use an operator to execute a Spark job, and the data is processed in Spark).
- A DAG is a data pipeline, an Operator is a task.
- An Executor defines how your tasks are executed, whereas a worker is a process executing your task
- The Scheduler schedules your tasks, the web server serves the UI, and the database stores the metadata of Airflow.

### Airflow Shutdown

D: && cd D:\development\Real_Time_Analysis\Airflow\docker
docker-compose down

[+] Running 8/8
 ✔ Container docker-airflow-triggerer-1  Removed
 ✔ Container docker-airflow-worker-1     Removed
 ✔ Container docker-airflow-webserver-1  Removed
 ✔ Container docker-airflow-scheduler-1  Removed
 ✔ Container docker-airflow-init-1       Removed
 ✔ Container docker-postgres-1           Removed
 ✔ Container docker-redis-1              Removed
 ✔ Network docker_default                Removed

### 28. DAG Skeleton (Command -> Admin)

pip install apache-airflow

### 30. Providers

<https://airflow.apache.org/docs/apache-airflow-providers/installing-from-sources.html>

// Airflow Core

pip install apache-airflow

// Airflow Providers <https://pypi.org/search/?q=apache-airflow-providers> => pip install apache-airflow-providers-...
// Airflow Providers Examples

pip install apache-airflow-providers-alibaba
pip install apache-airflow-providers-amazon
pip install apache-airflow-providers-apache-pinot
pip install apache-airflow-providers-apache-kafka
pip install apache-airflow-providers-apache-flink
pip install apache-airflow-providers-redis

### 31. Create a Table

pip install apache-airflow-providers-postgres

### 32. Create a connection

<http://localhost:8080/connection/list/>

Admin => Connections => + Add a new record

- Connection Id (postgres)
- Connection Type (Postgres)
- Host (postgres)
- Login (airflow)
- Password (airflow)
- Port (5432) => Test => Save

### 33. The secret weapon of Airflow

cd Airflow\docker
docker-compose ps
docker exec -it docker-airflow-scheduler-1 /bin/bash
  airflow@9fa7f9847faf:/opt/airflow$
    airflow -h
    airflow connections list
    airflow tasks test user_processing create_table 2023-01-01

### 35. Is the API available?

Go to the Airflow UI (on your machine localhost:80880) and create the following connection:

- Name: user_api
- Connection type: HTTP
- Host: <https://randomuser.me/>

### 37. Process users

### 40. Store users

### 42. Your DAG in action

D: && cd D:\development\Real_Time_Analysis\Airflow\docker
docker-compose ps
docker exec -it docker-airflow-worker-1 /bin/bash
  airflow@a751312e07d9:/opt/airflow$
    ls /tmp -l
    cat /tmp/processed_user.csv
      Roberta,Ramos,Brazil,silverpanda702,young,roberta.ramos@example.com
    exit

docker exec -it docker-postgres-1 /bin/bash
  root@8257b384ab82:/#
    psql -U airflow
    SELECT * FROM users;

      firstname | lastname | country |    username    | password |           email
      -----------+----------+---------+----------------+----------+---------------------------
      Roberta   | Ramos    | Brazil  | silverpanda702 | young    | roberta.ramos@example.com
      (1 row)

    exit

### Key Concepts of Datasets in Airflow

Dataset Definition:
  A dataset represents a logical collection of data that can be referenced by DAGs. It can be any data source such as a file, database table, or external data feed.

Dataset Producers:
  A DAG or task that updates or creates a dataset. When the dataset is updated, it can trigger downstream DAGs that are dependent on this dataset.

Dataset Consumers:
  DAGs that are triggered when a dataset is updated by a producer. Instead of relying on a fixed schedule, these DAGs run based on the data dependency.

### 51. Track your Datasets with the new view

Airflow UI => Datasets => /tmp/my_file.txt

### 54. What's an executor?

Executors are a critical component of Airflow, determining how and where tasks are executed. By choosing the appropriate executor, you can optimize Airflow for different environments and workloads, from single-machine setups to large, distributed systems.

Types of Executors in Airflow:

- SequentialExecutor: Executes tasks sequentially in a single process. Useful for debugging and testing.
- *LocalExecutor: Executes tasks in parallel using multiple processes on a single machine. Ideal for small-scale deployments.
- *CeleryExecutor: Executes tasks in parallel using multiple worker nodes. Suitable for large-scale deployments.
- *KubernetesExecutor: Executes tasks in parallel using Kubernetes pods. Ideal for containerized environments.
- DaskExecutor: Executes tasks in parallel using Dask distributed computing. 
  Use for dynamic scaling and integration with the Dask ecosystem.

### 55. The default config

docker cp docker-airflow-scheduler-1:/opt/airflow/airflow.cfg .
type airflow.cfg
  ...
  executor = SequentialExecutor
  ...

docker-compose.yaml
  ...
  environment:
    - AIRFLOW__CORE__EXECUTOR=CeleryExecutor # Overwrite the SequentialExecutor
  ...

### 56. The LocalExecutor

[core]
executor = CeleryExecutor
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@postgres/airflow
result_backend = db+postgresql://airflow:airflow@postgres/airflow

[celery]
broker_url = redis://:@redis:6379/0
result_backend = db+postgresql://airflow:airflow@postgres/airflow
default_queue = default
worker_concurrency = 16
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'

### 60. Add the DAG parallel_dag.py

### 61. Monitor your tasks with Flower

docker-compose down && docker-compose --profile flower up -d

[+] Running 9/9
 ✔ Network docker_default                Created
 ✔ Container docker-redis-1              Healthy
 ✔ Container docker-postgres-1           Healthy
 ✔ Container docker-airflow-init-1       Exited
 ✔ Container docker-airflow-worker-1     Started
 ✔ Container docker-flower-1             Started *
 ✔ Container docker-airflow-webserver-1  Started
 ✔ Container docker-airflow-scheduler-1  Started
 ✔ Container docker-airflow-triggerer-1  Started

<http://localhost:5555>

### 62. Remove DAG examples

docker-compose.yaml
...
//---
//# version: "3"
...
  AIRFLOW__CORE__LOAD_EXAMPLES: "false"
...

docker-compose --profile flower down && docker-compose --profile flower up -d

### 63. Running tasks on Celery Workers

docker-compose down && docker-compose --profile flower up -d
<http://localhost:5555>

### 65. Add a new Celery Worker

// Edit docker-compose.yaml

  ...
        condition: service_completed_successfully

  airflow-worker-1:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 10s
      timeout: 10s
      retries: 5
    environment:
      <<: *airflow-common-env
      # Required to handle warm shutdown of the celery workers properly
      # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
      DUMB_INIT_SETSID: "0"
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-worker-2:
    <<: *airflow-common
  ...

docker-compose --profile flower down && docker-compose --profile flower up -d

...
 ✔ Container docker-airflow-worker-2-1   Created
 ✔ Container docker-airflow-worker-1-1   Created
...

<http://localhost:5555>

### 66. Create a queue to better distribute tasks

// Edit docker-compose.yaml

  ...
  airflow-worker-2:
    <<: *airflow-common
    command: celery worker -q high_cpu
    healthcheck:
  ...

docker-compose --profile flower down && docker-compose --profile flower up -d

<http://localhost:5555>

from airflow.operators.bash_operator import BashOperator

### 67. Send a task to a specific queue

  ...
  transform = BashOperator(
      task_id='transform',
      queue='high_cpu', # Edit here...
      bash_command='sleep 10'
  )
  ...

docker-compose --profile flower down && docker-compose --profile flower up -d

<http://localhost:5555>

### 68. Concurrency parameters

Airflow Concurrency Parameters Summary:

1. parallelism / AIRFLOW__CORE__PARALLELISM:
   - Defines the maximum number of task instances that can run per scheduler.
   - Default: 32 tasks.
   - Total tasks = Number of schedulers × 32.
   - Depends on available resources and number of schedulers.

2. max_active_tasks_per_dag / AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG:
   - Sets the maximum number of concurrent task instances in each DAG.
   - Default: 16 tasks per DAG.

3. max_active_runs_per_dag / AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG:
   - Limits the number of active DAG runs per DAG.
   - Default: 16 active DAG runs per DAG.

### Assignment 2: [Practice] Group tasks with SubDAGs

// Edit docker-compose.yaml

  ---
  version: "3" # Edit here ...
  x-airflow-common: &airflow-common
  ...

### 74. Sharing data between tasks with XComs

XCom (short for "cross-communication") is a feature that allows tasks to exchange small amounts of data, such as messages or status information, during the execution of a DAG (Directed Acyclic Graph). XComs are a powerful way to pass information between tasks in a DAG, making it possible to create more dynamic and flexible workflows.

// Store MetaData ONLY

- PostgresSQL 1G
- SQLite 2G
- MySQL 64K

Key Features:

1. Data Exchange:
   - XComs enable tasks to push and pull data to and from a centralized storage managed by Airflow.
   - Each XCom is identified by a key and is associated with a specific DAG run and task instance.

2. Push and Pull Operations:

   - Push: Tasks can push data to XCom using the xcom_push method.
   - Pull: Tasks can retrieve data from XCom using the xcom_pull method.

3. Serialization:

   - XComs can handle various types of data, including strings, numbers, dictionaries, and other serializable objects.
   - The data is stored in the Airflow metadata database, making it accessible to other tasks within the same DAG run.

### 81. Running Elasticsearch with Airflow

// Edit docker-compose.yaml
...
services:
  //# Add Elasticsearch to the stack
  elastic:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.3.3
    environment:
      - "xpack.security.enabled=false"
      - "discovery.type=single-node"
      - "ES_JAVA_OPTS=-Xms750m -Xmx750m"
    ports:
      - 9200:9200
..
docker-compose --profile flower down && docker-cmpose --profile flower up -d
[+] Running 11/11
 ✔ Network docker_default                Create
 ✔ Container docker-postgres-1           Health
 ✔ Container docker-redis-1              Health
 ✔ Container docker-elastic-1            Started ***
 ✔ Container docker-airflow-init-1       Exited
 ✔ Container docker-airflow-scheduler-1  Started
 ✔ Container docker-airflow-worker-1-1   Started
 ✔ Container docker-flower-1             Started
 ✔ Container docker-airflow-webserver-1  Started
 ✔ Container docker-airflow-triggerer-1  Started
 ✔ Container docker-airflow-worker-2-1   Started

docker exec -it docker-airflow-scheduler-1 /bin/bash
  airflow@9fa7f9847faf:/opt/airflow$
    curl -X GET http://elastic:9200

      ...
      {
        "name" : "647f0ff2bd64",
        "cluster_name" : "docker-cluster",
        "cluster_uuid" : "R6CTV5pfQK-lMWMKDz_Vzw",
        "version" : {
          "number" : "8.3.3",
          "build_flavor" : "default",
          "build_type" : "docker",
          "build_hash" : "801fed82df74dbe537f89b71b098ccaff88d2c56",
          "build_date" : "2022-07-23T19:30:09.227964828Z",
          "build_snapshot" : false,
          "lucene_version" : "9.2.0",
          "minimum_wire_compatibility_version" : "7.17.0",
          "minimum_index_compatibility_version" : "7.0.0"
        },
        "tagline" : "You Know, for Search"
      }
      ...

    exit

### 83. Create the Elastic connection

Admin => Connections => + Add a new record

- Connection Id (elastic_default)
- Connection Type (HTTP)
- Host (http://elastic:9200)
- Port (9200) => Save

pip install apache-airflow-providers-http
test_elastic_connection from Airflow UI => success

### 84. Create the ElasticHook

pip install elasticsearch

\plugins\hooks\elastic_hook.py

### 85. Add ElasticHook to the Plugin system

docker-compose ps
docker exec -it docker-airflow-scheduler-1 /bin/bash
  airflow@9fa7f9847faf:/opt/airflow$
    airflow plugins
      No plugins loaded
    exit

// Edit \plugins\hooks\elastic_hook.py
...
class ElasticPlugin(AirflowPlugin):
    name = "elastic"
    hooks = [ElasticHook]

docker-compose --profile flower down && docker-compose --profile flower up -d

docker exec -it docker-airflow-scheduler-1 /bin/bash
airflow@f34f9791b21a:/opt/airflow$ 
  airflow plugins
    name    | hooks                    | source
    ========+==========================+==============================================
    elastic | elastic_hook.ElasticHook | $PLUGINS_FOLDER/hooks/elastic/elastic_hook.py
  exit

### 86. Add the DAG elastic_dag.py & Hook in Action
