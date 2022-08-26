from logsight.analytics_core.modules.log_statistics.template_stats \
    import TemplateStatistics
from logsight.analytics_core.modules.risk_analysis.risk_analysis import RiskAnalysis
from result_api.log_verification.group_stats import calculate_state_stats, calculate_total_messages, \
    count_template_stats, \
    frequency_statistics, risk_statistics
from result_api.log_verification.helpers import merge_template_stats
from result_api.log_verification.lambdas import calculate_state, get_change_perc, get_percentage, get_code_link


def calculate_compare_stats(baseline, candidate):
    # calculate base statistics for template
    baseline_stats = TemplateStatistics.calculate(baseline)
    candidate_stats = TemplateStatistics.calculate(candidate)

    # merge the base stats
    merged = merge_template_stats(baseline_stats, candidate_stats)

    # calculate new individual stats
    merged = calculate_individual_stats(merged)

    # grouped state stats

    group_stats = calculate_group_stats(merged)
    merged = merged[['risk_score', 'state', 'percentage_baseline', 'percentage_candidate', 'template', 'code_location',
                     'count_baseline', 'count_candidate', 'freq_change', 'coverage_baseline', 'coverage_candidate',
                     'level', 'predicted_anomaly']]

    group_stats['rows'] = merged.to_dict(orient='records')
    return group_stats


def calculate_group_stats(merged):
    total_n_log_messages = calculate_total_messages(merged)
    added_states = calculate_state_stats(merged, "added")
    deleted_states = calculate_state_stats(merged, "deleted")
    recurring_states = calculate_state_stats(merged, "recurring")
    count_baseline, count_candidate, total_count, candidate_perc_increase = count_template_stats(merged)

    freq_stats = frequency_statistics(merged)

    risk_stats = risk_statistics(merged)
    return dict(
        risk=risk_stats,
        total_n_log_messages=int(total_n_log_messages),
        count_baseline=int(count_baseline),
        count_candidate=int(count_candidate),
        candidate_perc=candidate_perc_increase,
        added_states=added_states['total'],
        added_states_info=added_states['info'],
        added_states_fault=added_states['fault'],
        deleted_states=deleted_states['total'],
        deleted_states_info=deleted_states['info'],
        deleted_states_fault=deleted_states['fault'],
        recurring_states=recurring_states['total'],
        recurring_states_info=recurring_states['info'],
        recurring_states_fault=recurring_states['fault'],
        frequency_change=freq_stats['frequency_change'],
        frequency_change_info=freq_stats['info'],
        frequency_change_fault=freq_stats['fault'],
    )


def calculate_individual_stats(merged):
    merged['state'] = merged.apply(lambda row: calculate_state(row['template_baseline'], row['template_candidate']),
                                   axis=1)
    merged['freq_change'] = merged.apply(lambda row: get_change_perc(row['count_baseline'], row['count_candidate']),
                                         axis=1)
    merged['percentage_baseline'] = merged.apply(
        lambda row: get_percentage(row['count_baseline'], row['count_candidate']),
        axis=1)
    merged['percentage_candidate'] = 100 - merged['percentage_baseline']
    ra = RiskAnalysis()
    merged['risk_score'] = merged.apply(
        lambda row: ra.calculate_verification_risk(row['state'], row['predicted_anomaly'], row['level']),
        axis=1)
    merged['code_location'] = merged.apply(lambda row: get_code_link(row['template_candidate']), axis=1)
    return merged
