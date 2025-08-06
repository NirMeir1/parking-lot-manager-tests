"""Tests for starting parking sessions."""

import pytest

from utils.api import start_parking


def test_tc1_start_parking_valid(session, base_url, unique_plate):
    """TC1 – Start Parking (Valid)."""
    response = start_parking(session, base_url, unique_plate)
    assert response.status_code == 200
    assert unique_plate in response.text


def test_tc2_duplicate_start_same_user(session, base_url, unique_plate):
    """TC2 – Duplicate Start (Same User)."""
    start_parking(session, base_url, unique_plate)
    duplicate = start_parking(session, base_url, unique_plate)
    assert duplicate.status_code >= 400 or "already" in duplicate.text.lower()


def test_tc3_duplicate_start_different_user(session, alt_session, base_url, unique_plate):
    """TC3 – Duplicate Start (Different User)."""
    start_parking(session, base_url, unique_plate)
    duplicate = start_parking(alt_session, base_url, unique_plate)
    assert duplicate.status_code >= 400 or "already" in duplicate.text.lower()
