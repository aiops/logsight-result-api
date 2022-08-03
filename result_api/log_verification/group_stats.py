import math

import numpy as np

from result_api.log_verification.helpers import filter_info_anomaly


def calculate_freq_change(df, total_freq_change):
    if total_freq_change == 0 or len(df) == 0:
        return 0, 0
    increase_perc = np.ceil(100 * len(df.loc[df['freq_change'] >= 0]) / total_freq_change).astype(float)
    decrease_perc = np.floor(100 * len(df.loc[df['freq_change'] < 0]) / total_freq_change).astype(float)
    return increase_perc, decrease_perc


def calculate_state_stats(merged, state="added"):
    state_df = merged.loc[merged['state'] == state]
    total_states = len(state_df)
    if not total_states:
        info_perc, fault_perc = 0, 0
    else:
        info_states = filter_info_anomaly(state_df)
        info_perc = math.floor(len(info_states) / total_states) * 100
        fault_perc = 100 - info_perc
    return {
        "info": info_perc,
        "fault": fault_perc,
        "total": total_states
    }


def count_template_stats(merged):
    count_baseline = merged['count_baseline'].sum()
    count_candidate = merged['count_candidate'].sum()
    total_count = count_baseline + count_candidate
    baseline_perc = int(100 * (count_baseline / total_count))
    candidate_perc_increase = (100 - baseline_perc) - baseline_perc
    return count_baseline, count_candidate, total_count, candidate_perc_increase


def frequency_statistics(merged, threshold=.25):
    freq_change_relevant = merged.loc[abs(merged['freq_change']) >= threshold].loc[merged['state'] == 'recurring']
    freq_change = len(freq_change_relevant)

    info_freq_df = filter_info_anomaly(freq_change_relevant)
    info_freq_increase, info_freq_decrease = calculate_freq_change(info_freq_df, freq_change)

    fault_freq_df = freq_change_relevant.loc[(freq_change_relevant['level'] != 'INFO') | (
            freq_change_relevant['predicted_anomaly'] == 1)]

    fault_freq_increase, fault_freq_decrease = calculate_freq_change(fault_freq_df, freq_change)

    return {"frequency_change": freq_change,
            "fault": {"increase": fault_freq_increase, "decrease": fault_freq_decrease},
            "info": {"increase": info_freq_increase, "decrease": info_freq_decrease}}


def risk_statistics(merged):
    max_risk = merged['risk_score'].max()
    avg_risk = merged['risk_score'].mean()

    return int(max_risk + min(avg_risk, 100 - max_risk))


def calculate_total_messages(merged):
    return merged[['count_baseline', 'count_candidate']].sum().sum()
