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
docker exec -it airflow-scheduler /bin/bash
  airflow@9fa7f9847faf:/opt/airflow$
    airflow -h
    airflow connections list
    airflow tasks test user_processing create_table 2023-01-01

### 35. Is the API available?

Airflow UI (on your machine localhost:80880) => Admin => Connections => +
Create the following connection:

- Connection Id: user_api
- Connection type: HTTP
- Host: <https://randomuser.me/>
=> Save

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

### 50. Create the Consumer DAG

Airflow UI

// Run producer => consumer
// Run producer2 => consumer2

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

docker cp airflow-scheduler:/opt/airflow/airflow.cfg .
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

docker exec -it airflow-scheduler /bin/bash
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

Airflow UI => Admin => Connections => + Add a new record

- Connection Id (elastic_default)
- Connection Type (HTTP)
- Host (elastic)
- Port (9200) => Save

pip install apache-airflow-providers-http
test_elastic_connection from Airflow UI => success

### 84. Create the ElasticHook

pip install elasticsearch

\plugins\hooks\elastic_hook.py

docker exec -it airflow_scheduler /bin/bash
  airflow plugins
    name    | hooks                    | source
    ========+==========================+==============================================
    elastic | elastic_hook.ElasticHook | $PLUGINS_FOLDER/hooks/elastic/elastic_hook.py

### 85. Add ElasticHook to the Plugin system

docker-compose ps
docker exec -it airflow-scheduler /bin/bash
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

docker exec -it airflow-scheduler /bin/bash
airflow@f34f9791b21a:/opt/airflow$ 
  airflow plugins
    name    | hooks                    | source
    ========+==========================+==============================================
    elastic | elastic_hook.ElasticHook | $PLUGINS_FOLDER/hooks/elastic/elastic_hook.py
  exit

### 86. Add the DAG elastic_dag.py & Hook in Action

### Revise docker-compose.yaml with container-name

docker-compose --profile flower down && docker-compose --profile flower up -d

[+] Running 11/11
 ✔ Network docker_default       Created
 ✔ Container airflow_postgres   Healthy
 ✔ Container airflow_redis      Healthy
 ✔ Container airflow_elastic    Started
 ✔ Container airflow_init       Exited
 ✔ Container airflow_flower     Started
 ✔ Container airflow_webserver  Started
 ✔ Container airflow_worker-2   Started
 ✔ Container airflow_scheduler  Started
 ✔ Container airflow_triggerer  Started
 ✔ Container airflow_worker-1   Started

docker exec -it airflow_scheduler /bin/bash
  airflow dags list
  cd dags
  ls -l
  exit

### BaseOperator

<https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html>
<https://github.com/apache/airflow/blob/main/airflow/models/baseoperator.py>

// Parameters

- task_id (str) – a unique, meaningful id for the task

- owner (str) – the owner of the task. Using a meaningful description (e.g. user/person/team/role name) to clarify ownership is recommended.
- email (str | Iterable[str] | None) – the ‘to’ email address(es) used in email alerts. This can be a single email or multiple ones. Multiple addresses can be specified as a comma or semicolon separated string or by passing a list of strings.
- email_on_retry (bool) – Indicates whether email alerts should be sent when a task is retried
- email_on_failure (bool) – Indicates whether email alerts should be sent when a task failed
...
- pre_execute (TaskPreExecuteHook | None) – a function to be called immediately before task execution, receiving a context dictionary; raising an exception will prevent the task from being executed. This is an experimental feature.
- post_execute (TaskPostExecuteHook | None) – a function to be called immediately after task execution, receiving a context dictionary and task result; raising an exception will prevent the task from succeeding.
...

### Task ID Limitations

- Unique: Task ID must be unique within a single Dag.
- Length: Task IDs must be less than 250 characters.
- Characters: Task IDs can only contain alphanumeric characters, dashes, and underscores.
- Start Character: Task IDs should start with an alphanumeric character.
- List [] >> List [] is not supported in Dag

### Owner

- Task Ownership and Permissions
  - The owner field in the tasks’ definitions (test_task_v01 has owner='mark' and test_task_v02 has owner='john') primarily serves as metadata. It doesn’t restrict task execution based on user permissions out of the box.
  - In standard Airflow setups, task execution is controlled by the scheduler, and any user with access to trigger the DAG can trigger the entire DAG, regardless of the individual task owners.

- Airflow Security Model
  - Default Behavior: By default, Airflow does not enforce task-level permissions based on the owner attribute.
  - RBAC (Role-Based Access Control): If RBAC is enabled in Airflow, permissions to trigger DAGs can be managed more granularly.

However, by default, triggering a DAG means all tasks in the DAG are subject to execution.

### Retry

retries = 3 # Attempt 4 times

### Email

<https://www.youtube.com/watch?v=xJrcExbQzKE&ab_channel=SriwWorldofCoding>
<https://myaccount.google.com/apppasswords>

- App Name (airflow_wsl2) => Create => Copy mhggxiwpjiqz.... => Done

// Edit airflow.cfg

[smtp]

smtp_host = smtp.gmail.com
smtp_starttls = True
smtp_ssl = False
smtp_user = samfire5200@gmail.com
smtp_password = mhggxiwpjiqz...
smtp_port = 587
smtp_mail_from = samfire5200@gmail.com

// Edit docker-compose.yaml

  volumes:
    ...
    - ./data:/opt/airflow/data
    - ./airflow.cfg:/opt/airflow/airflow.cfg # Edit here...
    ...

// Email settings

- email = '[]'
- email_on_retry = False/True
- email_on_failure = False/True
  
// Control levels

- airflow.cfg
- by dag => default_args
- by task

// Add files - Email Templates

<https://github.com/apache/airflow/blob/main/airflow/models/taskinstance.py>

- content_template_email.txt
- subject_template_email.txt

// Edit airflow.cfg

- subject_template = /opt/airflow/includes/subject_template_email.txt
- html_content_template = /opt/airflow/includes/content_template_email.txt

### Make your tasks dependent between DAGRuns

// test_dag_v2.0.py
...
    schedule_interval='@daily',
    dagrun_timeout=timedelta(seconds=60), ## Important here...
    catchup=True,

...
    task_c = PythonOperator(
        owner='mark',
        task_id='task_c',
        python_callable=_test_task,
        depends_on_past=True, ## Important here...
    )

### 16. Wait for downstream tasks

// test_dag_v2.0.py
with DAG(
    ...
    # dagrun_timeout=timedelta(seconds=60), # Remark here...
    catchup=True,
) as dag:

    task_a = BashOperator(
        owner='mark',
        task_id='task_a',
        bash_command='echo "Task A" && sleep 5',
        wait_for_downstream=True, # Change here...

    )
...

### 17. Pool party

// test_dag_v2.1.py
Airflow UI => Admin => Pools => + Add a new record

- Pool (process_tasks)
- Slots (1)
- Description (Pool to run Process Tasks sequentially - test_dag_v2.1.py)
=> Save

### 18. Task priority

// test_dag_v2.1.py
priority_weight = ...

### 22. Set expectations to your tasks with SLAs

// test_dag_v3.0.py

### 23. Timeout

// test_dag_v2.3.py for extract_a and extract_b

    ...
        wait_for_downstream=True,
        execution_timeout=timedelta(seconds=15) # Timeout for the task
    ...

### Callbacks

<https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html#callback-types>

- on_success_callback           Invoked when the task succeeds
- on_failure_callback           Invoked when the task fails
- on_retry_callback             Invoked when the task is up for retry
- on_execute_callback           Invoked right before the task begins executing.
- sla_miss_callback             Invoked when a task misses its defined SLA

### 28. Limit the concurrency

- Pools are used to limit the number of tasks that can be run concurrently in a DAG.
  Pools control concurrency across multiple tasks, potentially spanning multiple DAGs, based on shared resources.
- Tasks_concurrency is used to limit the number of tasks that can be run concurrently in a specific task.
  Controls concurrency at the level of individual tasks within a single DAG. (i.e. backward's start_date with Catchup=True)
  (for example: eLoan accrued and post interests) => tasks_concurrency=1

### 29. Chain and Cross dependency helpers

cross_downstream([t0 ], [t1, t2])
cross_downstream([t0, t1, t2], [t3, t4])
chain(t0, [t1, t2], [t3, t4])

### Providers

<https://registry.astronomer.io/>
<https://airflow.apache.org/docs/apache-airflow-providers-amazon/8.24.0/operators/index.html>

Example
<https://registry.astronomer.io/dags/snowflake_write_audit_publish/versions/1.4.0>

### 32. Introduction to Providers - build owned Docker Images

<https://airflow.apache.org/docs/docker-stack/build.html#build-build-image>

// Test Dockerfile first
docker build -t my-airflow:2.4.2 .

docker image ls | grep my-airflow
  my-airflow            2.4.2    2f34ece5dc6d   28 minutes ago   1.14GB

docker image rm my-airflow:2.4.2

// Edit docker-compose.yaml
...
x-airflow-common: &airflow-common
  ...
  // image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.5.1}
  build: .
...

docker-compose --profile flower down && docker-compose --profile flower up -d

docker exec airflow_scheduler airflow info
  apache-airflow-providers-amazon          | 6.0.0 ***
  apache-airflow-providers-celery          | 3.0.0
  apache-airflow-providers-cncf-kubernetes | 4.4.0
  ...
  apache-airflow-providers-elasticsearch   | 4.2.1
  apache-airflow-providers-ftp             | 3.1.0
  apache-airflow-providers-google          | 8.4.0
  apache-airflow-providers-grpc            | 3.0.0
  apache-airflow-providers-hashicorp       | 3.1.0
  apache-airflow-providers-http            | 4.0.0 ***
  apache-airflow-providers-imap            | 3.0.0
  apache-airflow-providers-microsoft-azure | 4.3.0
  apache-airflow-providers-mysql           | 3.2.1
  apache-airflow-providers-odbc            | 3.1.2
  apache-airflow-providers-postgres        | 5.2.2 ***
  apache-airflow-providers-redis           | 3.0.0
  ...

### 33. The PythonOperator

// my_python_dag_v0.py

docker exec -it airflow_scheduler /bin/bash

  airflow tasks test my_python_dag_v.0 task_a 2024-06-01
  ...
  Execution month-day: 6-1, Task Id: task_a
  [2024-06-11 08:34:09,687] {python.py:177} INFO - Done. Returned value was: None
  [2024-06-11 08:34:09,688] {taskinstance.py:1406} INFO - Marking task as SUCCESS. dag_id=my_python_dag_v.0, task_id=task_a, execution_date=20240601T000000, start_date=, end_date=20240611T083409

Airflow UI => Admin => Variables => + Add a new record

- '+' => Key (path) / Value (/usr/local/airflow/data) => Save
- '+' => Key (filename) / Value (my_data.csv) => Save
- '+' => Key (my_settings) / Value (
  {
  "path": "/usr/local/airflow/data",
  "filename": "my_data.csv"
  }
) => Save

### 34. The PythonOperator with the TaskFlow API (Decorator)

// my_python_dag_v1.py

airflow tasks test my_python_dag_v_1 task_a 2024-06-01
  ...
  Path: /usr/local/***/data, Filename: my_data.csv
  Logical date's month-day: 6-1, Task Id: task_a
  [2024-06-11 09:57:36,233] {python.py:177} INFO - Done. Returned value was: None
  [2024-06-11 09:57:36,233] {taskinstance.py:1406} INFO - Marking task as SUCCESS. dag_id=my_python_dag_v_1, task_id=task_a, execution_date=20240601T000000, start_date=, end_date=20240611T095736

airflow tasks test my_python_dag_v_1 store 2024-06-01

### 35. The BashOperator

Airflow UI => Admin => Variables => + Add a new record
=> '+' => Key (api_key_aws) / Value (echo "123456789012345678901234")
=> Save

airflow tasks test my_bash_dag_v_0 execute_command 2024-06-01
  ...
  [2024-06-11 11:53:28,391] {subprocess.py:86} INFO - Output:
  [2024-06-11 11:53:28,391] {subprocess.py:93} INFO - Execute command
  [2024-06-11 11:53:28,392] {subprocess.py:93} INFO - Task Id: execute_command
  [2024-06-11 11:53:28,392] {subprocess.py:93} INFO - AWS API Key: ***# Protected info
  [2024-06-11 11:53:28,392] {subprocess.py:93} INFO - Who am I?
  [2024-06-11 11:53:28,392] {subprocess.py:93} INFO - ***# Protected info
  [2024-06-11 11:53:28,393] {subprocess.py:93} INFO - AIRFLOW_CTX_DAG_OWNER=mark
  [2024-06-11 11:53:28,393] {subprocess.py:93} INFO - AIRFLOW_CTX_DAG_RUN_ID=__***...
  [2024-06-11 11:53:28,393] {subprocess.py:93} INFO - PWD=/tmp/***tmp2b8jup82
  [2024-06-11 11:53:28,394] {subprocess.py:93} INFO - aws_key=***# Protected info
  [2024-06-11 11:53:28,394] {subprocess.py:93} INFO - AIRFLOW_CTX_TRY_NUMBER=1
  ...

### 36. Quick note about templated fields

<https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html>
<https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html>

### Docker Operations

cd docker\stock_image
docker build -t stock_image:1.0.0 .

docker run --rm -v /d/development/Real_Time_Analysis/Airflow/docker/stock_image/scripts:/tmp/scripts stock_image:1.0.0 bash /tmp/scripts/output.sh

  Hello from the output.sh script!

### Docker in Docker

<https://medium.com/@shivam77kushwah/docker-inside-docker-e0483c51cc2c>
docker pull docker:dind
docker run --privileged --name dind-test -d docker:dind
docker exec dind-test docker run hello-world
docker exec dind-test docker images
docker rm dind-test -f

<https://devopscube.com/run-docker-in-docker/>
docker run --privileged -d --name dind-test docker:dind
docker exec -it dind-test /bin/sh
  docker run hello-world
  docker images
  exit

docker exec dind-test docker images
docker rm dind-test -f

### 37. The PostgresOperator

<https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html>

// Access Postgres from the command line
docker exec -it airflow_postgres /bin/bash
  psql -U airflow
    \l
    \c airflow
    \dt
    SELECT * FROM users;
    \q
    exit
  exit
  