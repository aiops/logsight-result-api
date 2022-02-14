import logging
import os
import time
import unittest

from result_api.config import global_vars
from result_api.configurator import ConnectionConfig
from result_api.continuous_verification.es_query import ElasticsearchDataSource
from result_api.continuous_verification.jorge import ContinuousVerification

logger = logging.getLogger("logsight." + __name__)


def verify_file_ext(filename: str, ext: str):
    filename += ext if not filename.endswith(ext) else ""
    return filename


class TestVerification(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        connection_conf_file = verify_file_ext("connections.json", ".json")
        self.cv_module = ContinuousVerification(connection_conf_file)
        es_client = ElasticsearchDataSource(
            **ConnectionConfig(os.path.join(global_vars.CONFIG_PATH, connection_conf_file)).get_elasticsearch_params())
        self.key = "mykey"
        self.app_name = "myapp"
        self.baselineTag = "default"
        self.compareTag = "default"
        self.index = self.key + "_" + self.app_name + "_" + "log_ad"
        docs = [{
            "app_name": "v",
            "application_id": "d486a039-c3ed-4626-b449-b99a832a8cb6",
            "private_key": "mpebhzyzyg82xsmfngvyztdeye",
            "logFormat": "UNKNOWN_FORMAT",
            "tag": "default",
            "receiptId": 2,
            "message": "[ 2822.783105] [UFW BLOCK] IN=wlp2s0 OUT= MAC=01:00:5e:00:00:01:98:9b:cb:c7:bb:33:08:00 SRC=192.168.178.1 DST=224.0.0.1 LEN=32 TOS=0x00 PREC=0xC0 TTL=1 ID=2526 DF PROTO=2",
            "field_parser": "syslog",
            "logsource": "sasho",
            "program": "kernel",
            "_failed_field_parsing": [
                "syslog"
            ],
            "@timestamp": "2022-02-05T15:33:05.000000",
            "actual_level": "INFO",
            "template": "[ <*> [UFW BLOCK] IN = <*> OUT = MAC = <*> SRC = <*> DST = <*> LEN = <*> TOS = <*> PREC = <*> TTL = <*> ID = <*> DF PROTO = <*>",
            "prediction": 0
        }, {
            "app_name": "v",
            "application_id": "d486a039-c3ed-4626-b449-b99a832a8cb6",
            "private_key": "mpebhzyzyg82xsmfngvyztdeye",
            "logFormat": "UNKNOWN_FORMAT",
            "tag": "default",
            "receiptId": 2,
            "message": "[ 2822.783105] [UFW BLOCK] IN=wlp2s0 OUT= This is a failed log message",
            "field_parser": "syslog",
            "logsource": "sasho",
            "program": "kernel",
            "_failed_field_parsing": [
                "syslog"
            ],
            "@timestamp": "2022-02-05T15:33:05.000000",
            "actual_level": "INFO",
            "template": "[ <*> [UFW BLOCK] IN = <*> OUT = MAC = <*> SRC = <*> DST = <*> LEN = <*> TOS = <*> PREC = <*> TTL = <*> ID = <*> DF PROTO = <*>",
            "prediction": 1
        }]
        for d in docs:
            es_client.es.index(self.index, d)

    def test_verification_valid(self):
        params = [[self.key, self.app_name, self.compareTag, self.baselineTag]]
        for param in params:
            cv_run = self.cv_module.run_verification(param[0], param[1], param[2], param[3])
            assert cv_run is not None
            print(cv_run)

    def test_verification_invalid_all_params(self):
        params = [["", "", "", ""], [self.key, self.app_name, self.compareTag, ""],
                  [self.key, self.app_name, "", self.baselineTag],
                  [self.app_name, self.key, self.compareTag, self.baselineTag]]
        for param in params:
            assert self.cv_module.run_verification(param[0], param[1], param[2], param[3]) is None


if __name__ == "__main__":
    unittest.main()
