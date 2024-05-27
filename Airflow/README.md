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

### Installing Apache Airflow

cd Airflow\docker
docker-compose up -d
<http://localhost:8080>
