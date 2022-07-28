import pandas as pd
from io import StringIO

import pytest

from result_api.log_verification.helpers import filter_info_anomaly, merge_template_stats


@pytest.fixture
def baseline_stats():
    stats = """
    Adding block pool ,1,INFO,2,0.6666666
    Adding replicas to map for block pool,1,INFO,2,0.6666666
    Analyzing storage directories,1,INFO,2,0.6666
    Balancing bandwidth is <:NUM:> bytes/s,1,WARN,2,0.066666
    starting to offer service,1,INFO,2,0.66666
    beginning handshake with NN,1,INFO,2,0.66666
    successfully registered with NN,1,INFO,2,0.66666
    """
    yield pd.read_csv(StringIO(stats), header=None,
                      names=['template', 'predicted_anomaly', 'count', 'level', 'coverage'])


@pytest.fixture
def candidate_stats():
    stats = """
     Disabling file IO profiling,0,INFO,4,0.00133333
     Assuming default value of <:NUM:>,1,WARN,2,0.066666666
     Datanode Uuid unassigned,0,INFO,2,0.066666
     Added filter static_user_filter,0,INFO,2,0.66666
    """
    yield pd.read_csv(StringIO(stats), header=None,
                      names=['template', 'predicted_anomaly', 'count', 'level', 'coverage'])


def test_filter_info(candidate_stats):
    result = filter_info_anomaly(candidate_stats)
    assert 'WARN' not in result['level']
    assert 1 not in result['predicted_anomaly']
    assert len(result) != len(candidate_stats)


def test_merge_template_stats(baseline_stats, candidate_stats):
    merged = merge_template_stats(baseline_stats, candidate_stats)
    cols = ['count_baseline', 'count_candidate', 'coverage_baseline', 'coverage_candidate', 'level',
            'predicted_anomaly', 'template']
    assert merged[cols].isna().sum().sum() == 0
