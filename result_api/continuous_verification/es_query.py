import logging
import os
from typing import Dict

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

    def get_log_ad_data(self, private_key: str, app: str, tags: Dict[str, str]):
        self.es.indices.put_settings(index="_all",
                                     body={"index": {
                                         "max_result_window": 500000
                                     }})
        index = f"{private_key}_{app}*"
        filter_query = []
        for tag_key in tags:
            filter_query.append({"match_phrase": {f"tags.{tag_key}.keyword": tags[tag_key]}})
        res = self.es.search(
            index=index,
            doc_type='_doc',
            body={
                "size": os.environ.get("ES_QUERY_SIZE", 10000),
                "query": {
                    "bool": {
                        "must": [],
                        "filter": filter_query,
                        "should": [],
                        "must_not": []
                    }
                }
            }
        )

        return [r['_source'] for r in res['hits']['hits']]
