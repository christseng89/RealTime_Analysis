#!/bin/bash

echo "Current working directory: $(pwd)"
echo "Dag Id: {{dag.dag_id}}"
echo "Task Id: {{ti.task_id}}"
echo "Postgres Password: {{var.value.password_postgres}}"