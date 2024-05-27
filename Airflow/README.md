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
- Sensor Operators:
  - TimeSensor: Waits until a specific time.
  - S3KeySensor: Waits for a file to appear in an S3 bucket.

### Operator Summary

- Operators: Core components in Airflow DAGs that define the tasks to be performed.
- Types: Include Action Operators, Transfer Operators, Sensor Operators, DummyOperator, SubDagOperator, and other specific operators.
- Custom Operators: Can be created to handle specific needs not covered by built-in operators, providing flexibility to extend Airflow's capabilities.

### Installing Apache Airflow - via Terminal (Admin)

cd D:\development\Real_Time_Analysis\Airflow\docker
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

### Airflow Summary

- Airflow is an orchestrator, not a processing framework. Process your gigabytes of data outside of Airflow
  (i.e. You have a Spark cluster, you use an operator to execute a Spark job, and the data is processed in Spark).
- A DAG is a data pipeline, an Operator is a task.
- An Executor defines how your tasks are executed, whereas a worker is a process executing your task
- The Scheduler schedules your tasks, the web server serves the UI, and the database stores the metadata of Airflow.
