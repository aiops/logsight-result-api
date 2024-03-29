import os

DEBUG = False
USES_KAFKA = False
USES_ES = True
CONFIG_PATH = os.path.split(os.path.realpath(__file__))[0]
FILE_SINK_PATH = os.path.join(os.path.split(CONFIG_PATH)[0], "datastore")

RISK_SCORE_ADDED_STATE_LEVEL_INFO_SEMANTICS_REPORT = int(os.environ.get('RISK_SCORE_ADDED_STATE_LEVEL_INFO_SEMANTICS_REPORT', 0))
RISK_SCORE_ADDED_STATE_LEVEL_ERROR_SEMANTICS_REPORT = int(os.environ.get('RISK_SCORE_ADDED_STATE_LEVEL_ERROR_SEMANTICS_REPORT', 70))
RISK_SCORE_ADDED_STATE_LEVEL_INFO_SEMANTICS_FAULT = int(os.environ.get('RISK_SCORE_ADDED_STATE_LEVEL_INFO_SEMANTICS_FAULT', 60))
RISK_SCORE_ADDED_STATE_LEVEL_ERROR_SEMANTICS_FAULT = int(os.environ.get('RISK_SCORE_ADDED_STATE_LEVEL_ERROR_SEMANTICS_FAULT', 80))

RISK_SCORE_DELETED_STATE_LEVEL_INFO_SEMANTICS_REPORT = int(os.environ.get('RISK_SCORE_DELETED_STATE_LEVEL_INFO_SEMANTICS_REPORT', 0))
RISK_SCORE_DELETED_STATE_LEVEL_ERROR_SEMANTICS_REPORT = int(os.environ.get('RISK_SCORE_DELETED_STATE_LEVEL_ERROR_SEMANTICS_REPORT', 0))
RISK_SCORE_DELETED_STATE_LEVEL_INFO_SEMANTICS_FAULT = int(os.environ.get('RISK_SCORE_DELETED_STATE_LEVEL_INFO_SEMANTICS_FAULT', 0))
RISK_SCORE_DELETED_STATE_LEVEL_ERROR_SEMANTICS_FAULT = int(os.environ.get('RISK_SCORE_DELETED_STATE_LEVEL_ERROR_SEMANTICS_FAULT', 0))

RISK_SCORE_RECURRING_STATE_LEVEL_INFO_SEMANTICS_REPORT = int(os.environ.get('RISK_SCORE_RECURRING_STATE_LEVEL_INFO_SEMANTICS_REPORT', 0))
RISK_SCORE_RECURRING_STATE_LEVEL_ERROR_SEMANTICS_REPORT = int(os.environ.get('RISK_SCORE_RECURRING_STATE_LEVEL_ERROR_SEMANTICS_REPORT', 25))
RISK_SCORE_RECURRING_STATE_LEVEL_INFO_SEMANTICS_FAULT = int(os.environ.get('RISK_SCORE_RECURRING_STATE_LEVEL_INFO_SEMANTICS_FAULT', 25))
RISK_SCORE_RECURRING_STATE_LEVEL_ERROR_SEMANTICS_FAULT = int(os.environ.get('RISK_SCORE_RECURRING_STATE_LEVEL_ERROR_SEMANTICS_FAULT', 25))


VERIFICATION_RISK_THRESHOLD = int(os.environ.get('VERIFICATION_RISK_THRESHOLD', 80))
