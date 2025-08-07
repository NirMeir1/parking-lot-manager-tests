"""Tests for starting parking sessions."""

import pytest
from utils.api import start_parking, count_plate_occurrences


def test_tc1_start_parking_valid(session, base_url, unique_plate):
    """TC1 – Start Parking (Valid)."""
    response = start_parking(session, base_url, unique_plate)
    assert response.status_code == 200

    dashboard = session.get(f"{base_url}/")
    # TODO: replace HTML scraping with GET /api/parkings once available
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1


def test_tc2_duplicate_start_same_user(session, base_url, unique_plate):
    """TC2 – Duplicate Start (Same User)."""
    start_parking(session, base_url, unique_plate)
    second = start_parking(session, base_url, unique_plate)
    assert second.status_code == 200

    dashboard = session.get(f"{base_url}/")
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1


def test_tc3_duplicate_start_different_user(session, alt_session, base_url, unique_plate):
    """TC3 – Duplicate Start (Different User)."""
    start_parking(session, base_url, unique_plate)
    second = start_parking(alt_session, base_url, unique_plate)
    assert second.status_code == 200

    dashboard = alt_session.get(f"{base_url}/")
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1
