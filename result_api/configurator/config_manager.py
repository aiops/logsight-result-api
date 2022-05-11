from config import Config

from configs.global_vars import DEBUG


class ConnectionConfig:
    def __init__(self, connection_config_path: str):
        self.conns = Config(connection_config_path).as_dict()

        for conn in self.conns:
            for key in self.conns[conn].keys():
                if 'host' in key and DEBUG:
                    self.conns[conn][key] = "localhost"
                if 'url' in key and DEBUG:
                    self.conns[conn][key] = "localhost"

        if "kafka" in self.conns:
            self.conns['kafka']['address'] = f"{self.conns['kafka']['host']}:{self.conns['kafka']['port']}"

    def get_kafka_params(self):
        return self.conns['kafka']

    def get_elasticsearch_params(self):
        return self.conns['elasticsearch']

    def get_connection(self, conn):
        return self.conns.get(conn, {})

