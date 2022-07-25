import logging
import os
from typing import Dict

from elasticsearch import Elasticsearch


class ElasticsearchDataSource:

    def __init__(self, host, port, username, password):
        print(f"Connecting to {host}:{port} as user {username}")
        self.es = Elasticsearch(
            [{'scheme': 'http', 'host': host, 'port': int(port)}],
            http_auth=(username, password),
            timeout=30,
            max_retries=5,
            retry_on_timeout=True
        )

    def get_log_ad_data(self, private_key: str, tags: Dict[str, str]):
        index = f"{private_key}*_pipeline"
        self.es.indices.put_settings(index=index,
                                     body={"index": {
                                         "max_result_window": 500000
                                     }})
        filter_query = []
        for tag_key in tags:
            filter_query.append({"match_phrase": {f"tags.{tag_key}.keyword": tags[tag_key]}})
        res = self.es.search(
            index=index,
            body={
                "sort": [
                    {
                        "timestamp": {
                            "order": "asc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
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
