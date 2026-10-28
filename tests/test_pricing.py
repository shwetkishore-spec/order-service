"""Unit tests: run on every push and pull request by CI."""
import pytest

from app.pricing import calculate_total


def test_no_discount_at_or_below_500():
    assert calculate_total(500) == 500
    assert calculate_total(200) == 200


def test_discount_applied_above_500():
    assert calculate_total(600) == 540


def test_negative_cart_rejected():
    with pytest.raises(ValueError):
        calculate_total(-1)
