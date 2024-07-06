copy airflow-values1.yaml airflow-values1.bak /y
copy airflow-values2.yaml airflow-values1.yaml /y
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f airflow-values1.yaml
copy airflow-values1.yaml airflow-values2.yaml /y
copy airflow-values1.bak airflow-values1.yaml /y
del airflow-values1.bak