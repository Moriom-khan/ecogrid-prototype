from app.config import (
    API_LATENCY_TARGET_MS,
    EVENT_PROCESSING_TARGET_SECONDS,
    TEST_COVERAGE_TARGET
)


def test_api_latency_target_is_defined():

    assert API_LATENCY_TARGET_MS <= 500


def test_event_processing_target_is_defined():

    assert EVENT_PROCESSING_TARGET_SECONDS <= 5


def test_test_coverage_target_is_defined():

    assert TEST_COVERAGE_TARGET >= 80
