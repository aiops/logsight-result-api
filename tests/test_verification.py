import argparse
import logging
import os
import unittest
import uuid
from plistlib import Dict

from logsight_classes.data_class import AppConfig
from logsight_classes.responses import SuccessResponse, ErrorResponse
from result_api.config.global_vars import CONFIG_PATH
from result_api.configurator import ConnectionConfig
from result_api.continuous_verification.jorge import ContinuousVerification
from run import create_manager
from services.configurator import ManagerConfig

logger = logging.getLogger("logsight." + __name__)


def parse_arguments() -> Dict:
    parser = argparse.ArgumentParser(description='Logsight monolith result API.')
    parser.add_argument('--cconf', help='Connection config to use (filename in logsight/config directory)',
                        type=str, default='connections', required=False)
    args = vars(parser.parse_args())
    return args


def get_config(args: Dict) -> ConnectionConfig:
    connection_conf_file = verify_file_ext(args['cconf'], ".json")
    connection_conf_path = os.path.join(CONFIG_PATH, connection_conf_file)
    return ConnectionConfig(connection_conf_path)


def verify_file_ext(filename: str, ext: str):
    filename += ext if not filename.endswith(ext) else ""
    return filename


class TestVerification(unittest.TestCase):
    def test_create_application_pass(self):
        args = parse_arguments()
        connection_conf_file = verify_file_ext(args['cconf'], ".json")
        cv_module = ContinuousVerification(connection_conf_file)
        cv_module.run_verification()


if __name__ == "__main__":
    unittest.main()
