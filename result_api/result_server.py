import argparse
import json
import os

from flask import Flask, jsonify
from flask import request

from configurator import ConnectionConfig
from continuous_verification.jorge import ContinuousVerification
from typing import Dict
from config.global_vars import CONFIG_PATH
from dto.VerificationDTO import VerificationDTO
from result_api.config.global_vars import CONFIG_PATH
from result_api.responses.responses import ErrorResponse

app = Flask(__name__, template_folder="./")


@app.route('/api/v1/verification', methods=['POST'])
def get_tasks():
    args = request.data
    verificationDTO = VerificationDTO(**json.loads(request.data))
    result = cv_module.run_verification(application_id=verificationDTO.applicationName,
                                        private_key=verificationDTO.privateKey,
                                        baseline_tag_id=verificationDTO.baselineTag,
                                        compare_tag_id=verificationDTO.compareTag)
    if result:
        return jsonify(result)
    else:
        resp = {"message": "Data index does not exists, or empty. Try again later.", "status": 404}
        return jsonify(resp)


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


if __name__ == '__main__':
    from waitress import serve

    args = parse_arguments()
    config = get_config(args)

    connection_conf_file = verify_file_ext(args['cconf'], ".json")
    cv_module = ContinuousVerification(connection_conf_file)

    serve(app, host='0.0.0.0', port=5554)
