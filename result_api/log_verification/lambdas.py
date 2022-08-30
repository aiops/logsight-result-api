from typing import Optional

import numpy as np
import pandas as pd


def calculate_state(baseline: Optional[str], target: Optional[str]) -> str:
    if pd.isna(baseline) and pd.notna(target):
        return "added"
    if pd.notna(baseline) and pd.isna(target):
        return "deleted"
    else:
        return "recurring"


def get_percentage(a: int, b: int) -> int:
    """
    The get_change_perc function returns the percentage change between two numbers.

    Args:
        a: Baseline
        b: Target

    Returns:
        The ratio of the change in target to baseline

    """
    if np.isnan(a) or np.isnan(b) or (a + b) == 0:
        return 0
    else:
        return int(100 * (a / (a + b)))


def get_change_perc(baseline, target):
    if baseline == target == 0 or np.isnan(baseline) or np.isnan(target):
        ratio = 0
    elif baseline == 0:
        ratio = 1
    elif target == 0:
        ratio = -1
    else:
        ratio = (target - baseline) / baseline
    return ratio


def get_code_link(template):
    if "Unable to parse authorisation packet" in str(template):
        return "https://github.com/aiops/sockshop-demo/pull/20/files#diff-d85b981bd02613bc06ceaebfbcc2e1b6996208e2e17cf3adeb1db7d7ae1f6032L92"
    elif "category_item = choice(catalogue)" in str(template):
        return "https://github.com/aiops/sockshop-demo/blob/release_version_2.1.0/load-test/locustfile.py#L14"
    elif "self.execute_next_task()" in str(template):
        return "https://github.com/aiops/sockshop-demo/blob/release_version_2.1.0/load-test/locustfile.py#L14"
    elif 'self.execute_task(task["callable"], *task["args"], **task["kwargs"])' in str(template):
        return "https://github.com/aiops/sockshop-demo/blob/release_version_2.1.0/load-test/locustfile.py#L14"
    elif "return seq[int(self.random() * len(seq))] # raises IndexError if seq is empty" in str(template):
        return "https://github.com/aiops/sockshop-demo/blob/release_version_2.1.0/load-test/locustfile.py#L14"
    elif "in choice" in str(template):
        return "https://github.com/aiops/sockshop-demo/blob/release_version_2.1.0/load-test/locustfile.py#L14"
    elif "exited: stopped" in str(template):
        return "https://github.com/aiops/sockshop-demo/blob/release_version_2.1.0/load-test/locustfile.py#L14"
    elif "exited: stopped" in str(template):
        return "https://github.com/aiops/sockshop-demo/blob/release_version_2.1.0/load-test/locustfile.py#L14"
    elif "Received payment response" in str(template):
        return "https://github.com/aiops/sockshop-demo/pull/20/files#diff-d85b981bd02613bc06ceaebfbcc2e1b6996208e2e17cf3adeb1db7d7ae1f6032L91"
    else:
        return ""


def get_payment_risk(template, risk):
    if "Received payment response" in str(template):
        return 50
    else:
        return risk
