import numpy as np
import pytest

from result_api.log_verification.lambdas import calculate_state, get_change_perc, get_percentage


@pytest.mark.parametrize("a", [np.NaN, 0])
@pytest.mark.parametrize("b", [np.NaN, 0])
def test_get_change_perc_invalid(a, b):
    assert get_change_perc(a, b) == 0


@pytest.mark.parametrize("a,b,expected", [(8, 12, 0.5)])
def test_get_change_perc(a, b, expected):
    result = get_change_perc(a, b)
    assert result == expected
    assert isinstance(result, float)


@pytest.mark.parametrize("a", [np.NaN, 0])
@pytest.mark.parametrize("b", [np.NaN, 0])
def test_get_percentage_invalid(a, b):
    assert get_percentage(a, b) == 0


@pytest.mark.parametrize("a,b,expected", [(8, 12, 40)])
def test_get_percentage(a, b, expected):
    result = get_percentage(a, b)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize("baseline,target,expected", [("a", np.NaN, "deleted"),
                                                      (np.NaN, "a", "added"),
                                                      ("a", "a", "recurring"),
                                                      (np.NaN, np.NaN, "recurring")])
def test_calculate_state(baseline, target, expected):
    result = calculate_state(baseline, target)
    assert result == expected
    assert isinstance(result, str)
