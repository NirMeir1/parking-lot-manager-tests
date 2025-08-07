"""Tests related to *starting* parking sessions."""

from utils.api import start_parking, count_plate_occurrences


def test_tc1_start_parking_valid(session, base_url, unique_plate):
    """TC1 – Start Parking (Valid)."""
    resp = start_parking(session, base_url, unique_plate)
    assert resp.status_code == 200

    dashboard = session.get(f"{base_url}/")
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1


def test_tc2_duplicate_start_same_user(session, base_url, unique_plate):
    """TC2 – Duplicate Start (same user). 2nd request should be ignored."""
    start_parking(session, base_url, unique_plate)
    resp_second = start_parking(session, base_url, unique_plate)
    assert resp_second.status_code == 200

    dashboard = session.get(f"{base_url}/")
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1


def test_tc3_duplicate_start_different_user(
    session,
    alt_session,
    base_url,
    unique_plate,
):
    """TC3 – Duplicate Start (different user). Only one active session allowed."""
    start_parking(session, base_url, unique_plate)
    resp_second = start_parking(alt_session, base_url, unique_plate)
    assert resp_second.status_code == 200

    dashboard = alt_session.get(f"{base_url}/")
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1