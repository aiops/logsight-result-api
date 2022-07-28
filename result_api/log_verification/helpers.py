import pandas as pd


def filter_info_anomaly(df):
    return df.loc[(df['level'] == 'INFO') & (df['predicted_anomaly'] != 1)]


def merge_template_stats(baseline_stats, candidate_stats):
    merged = pd.merge(baseline_stats, candidate_stats, how='outer', left_index=True, right_index=True,
                      suffixes=('_baseline', '_candidate'))

    merged['level'] = merged['level_baseline'].combine_first(merged['level_candidate'])

    merged['predicted_anomaly'] = merged['predicted_anomaly_baseline'].combine_first(
        merged['predicted_anomaly_candidate'])

    cols = ['count_baseline', 'count_candidate', 'coverage_baseline', 'coverage_candidate']
    merged[cols] = merged[cols].fillna(0)

    merged['template'] = merged['template_baseline'].combine_first(merged['template_candidate'])

    return merged
