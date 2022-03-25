import argparse
import logging
import os
from http import HTTPStatus

from flask import Flask, jsonify, Response
from flask import request

from configurator import ConnectionConfig
from continuous_verification.jorge import ContinuousVerification
from typing import Dict
from dto.verification_dto import VerificationDTO
from configs.global_vars import CONFIG_PATH
from responses.responses import ErrorResponse

app = Flask(__name__, template_folder="./")


@app.route('/api/v1/compare', methods=['GET'])
def get_tasks():
    try:
        verificationDTO = VerificationDTO(**request.args)
    except Exception as e:
        logging.info(e)
        err = ErrorResponse(request.args.get("applicationId", ""), "Invalid parameters.")
        return Response(err.json(),status=HTTPStatus.NOT_FOUND)
    result = cv_module.run_verification(application_id=verificationDTO.applicationName,
                                        private_key=verificationDTO.privateKey,
                                        baseline_tag_id=verificationDTO.baselineTag,
                                        compare_tag_id=verificationDTO.compareTag)
    print(result)
    try:
        if result is not None:
            return jsonify(result)
        else:
            err = ErrorResponse(verificationDTO.applicationId, "Data index does not exists, or empty. Try again later.")
            return Response(err.json(),status=HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.error(f"jsonify of compare results failed. Reason: {e}")
        err = ErrorResponse(verificationDTO.applicationId, "Internal server error")
        return Response(err.json(),status=HTTPStatus.INTERNAL_SERVER_ERROR)


def parse_arguments() -> Dict:
    parser = argparse.ArgumentParser(description='Logsight monolith result API.')
    parser.add_argument('--cconf', help='Connection configs to use (filename in logsight/configs directory)',
                        type=str, default='connections', required=False)
    args = vars(parser.parse_args())
    return args


def get_config(args: Dict) -> ConnectionConfig:
    connection_conf_file = verify_file_ext(args['cconf'], ".cfg")
    connection_conf_path = os.path.join(CONFIG_PATH, connection_conf_file)
    return ConnectionConfig(connection_conf_path)


def verify_file_ext(filename: str, ext: str):
    filename += ext if not filename.endswith(ext) else ""
    return filename


if __name__ == '__main__':
    from waitress import serve

    args = parse_arguments()
    config = get_config(args)

    connection_conf_file = verify_file_ext(args['cconf'], ".cfg")
    cv_module = ContinuousVerification(connection_conf_file)

    serve(app, host='0.0.0.0', port=5554)
