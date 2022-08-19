import json
import logging
import math
from datetime import datetime, timedelta
import time

import pandas as pd
from elasticsearch import NotFoundError

from logsight.configs.properties import LogsightProperties
from result_api.configs.properties import ResultApiConfig
from result_api.log_verification.fn import calculate_compare_stats
from logsight.services import ElasticsearchService

PIPELINE_INDEX_EXT = LogsightProperties().pipeline_index_ext

logger = logging.getLogger("logsight." + __name__)


class NotFoundException(Exception):
    pass


class LogVerification:
    def __init__(self, es_service: ElasticsearchService):
        self.es_service = es_service
        self.th = ResultApiConfig().verification_risk_threshold

    def extract_data_for_tag(self, private_key, tags):
        index = "_".join([private_key, PIPELINE_INDEX_EXT])
        latest_ingest_time = str(datetime.min.isoformat())
        now = datetime.utcnow().replace(second=0, microsecond=0)

        logs = []
        while True:
            result = self.es_service.get_all_logs_for_tag(index, latest_ingest_time, str(now.isoformat()), tags=tags)
            logs.extend(result)
            if len(result) == 0:
                break
            latest_ingest_time = result[-1]['ingest_timestamp']

        if len(logs) > 0:
            logs_df = pd.DataFrame(logs).set_index('timestamp')
            logs_df.index = pd.to_datetime(logs_df.index)
            return logs_df[['level', 'template', 'tags', 'prediction']]

    def run_verification(self, private_key, baseline_tags, candidate_tags):
        start_time = time.time()
        if candidate_tags is None:
            candidate_tags = {}
        if baseline_tags is None:
            baseline_tags = {}
        if isinstance(baseline_tags, str):
            baseline_tags = json.loads(baseline_tags)
        if isinstance(candidate_tags, str):
            candidate_tags = json.loads(candidate_tags)

        try:
            df_baseline = self.extract_data_for_tag(private_key, baseline_tags)
            df_candidate = self.extract_data_for_tag(private_key, candidate_tags)
        except NotFoundError as e:
            raise NotFoundException(e.body['error']['reason'])
        if df_candidate is None or df_baseline is None:
            raise NotFoundException("Data index does not exists, or empty. Try again later.")
        time_delta_df_baseline = df_baseline.index[-1] - df_baseline.index[0] + timedelta(minutes=3)
        time_delta_df_candidate = df_candidate.index[-1] - df_candidate.index[0] + timedelta(minutes=3)
        try:
            if time_delta_df_candidate < time_delta_df_baseline:
                df_baseline = df_baseline.loc[(df_baseline.index >= df_baseline.index[0]) & (
                        df_baseline.index < (df_baseline.index[0] + time_delta_df_candidate))]
            else:
                df_candidate = df_candidate.loc[(df_candidate.index >= df_candidate.index[0]) & (
                        df_candidate.index < (df_candidate.index[0] + time_delta_df_baseline))]
        except Exception as e:
            logger.error(e)
            if len(df_baseline.index) < len(df_candidate.index):
                df_candidate = df_candidate[:len(df_baseline)]
            else:
                df_baseline = df_baseline[:len(df_candidate)]

        output = calculate_compare_stats(df_baseline, df_candidate)

        output['timestamp'] = datetime.utcnow().isoformat()
        output['baseline_tags'] = baseline_tags
        output['candidate_tags'] = candidate_tags
        output['tag_keys'] = list(baseline_tags.keys())
        output['tags'] = baseline_tags
        output['severity'] = math.ceil((output['risk'] + 0.01) / 34)
        output['velocity'] = time.time() - start_time
        output['is_failure'] = int(output['risk'] >= self.th)
        resp = self.es_service.parallel_bulk(output, private_key + "_verifications")
        output['compareId'] = resp['index']['_id']

        return output
