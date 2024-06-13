from airflow.plugins_manager import AirflowPlugin
from hooks.elastic.elastic_hook import ElasticHook

class ElasticPlugin(AirflowPlugin):
    name = "elastic"
    hooks = [ElasticHook]
