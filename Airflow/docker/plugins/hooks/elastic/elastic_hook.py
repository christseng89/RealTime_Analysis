from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base import BaseHook
from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):

    def __init__(self, conn_id='elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self.get_connection(conn_id)

        conn_config = {}
        hosts = []

        if conn.host:
            hosts = conn.host.split(',')
            scheme = 'http'  # Default scheme
            if conn.schema:
                scheme = conn.schema
            if conn.port:
                hosts = [f"{scheme}://{host}:{conn.port}" for host in hosts]
            else:
                hosts = [f"{scheme}://{host}" for host in hosts]

        if conn.login:
            conn_config['http_auth'] = (conn.login, conn.password)

        self.es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema

    def info(self):
        return self.es.info()

    def set_index(self, index):
        self.index = index

    def add_doc(self, index, doc_type, doc):
        self.set_index(index)
        res = self.es.index(index=index, doc_type=doc_type, doc=doc)
        return res
    
class ElasticPlugin(AirflowPlugin):
    name = "elastic"
    hooks = [ElasticHook]
