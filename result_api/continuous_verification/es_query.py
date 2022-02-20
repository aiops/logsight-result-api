from elasticsearch import Elasticsearch


class ElasticsearchDataSource:

    def __init__(self, host, port, username, password):
        print(f"Connecting to {host}:{port} as user {username}")
        self.es = Elasticsearch(
            [{'host': host, 'port': port}],
            http_auth=(username, password),
            timeout=30,
            max_retries=5,
            retry_on_timeout=True
        )

    def get_log_ad_data(self, private_key: str, app: str, tag: str):
        index = f"{private_key}_{app}_log_ad"
        res = self.es.search(
            index=index,
            doc_type='_doc',
            body={
                "size": 10000,
                "query": {
                    "match": {"tag": tag}
                }
            }
        )

        return [r['_source'] for r in res['hits']['hits']]