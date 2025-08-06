"""Tests for ending parking sessions."""

from utils.api import start_parking, end_parking, find_parking_id


def test_tc18_end_parking_valid(session, base_url, unique_plate):
    """TC18 – End Parking (Valid)."""
    start_parking(session, base_url, unique_plate)
    dashboard = session.get(f"{base_url}/")
    parking_id = find_parking_id(dashboard.text, unique_plate)
    assert parking_id is not None

    response = end_parking(session, base_url, parking_id)
    assert response.status_code == 200

    verify = session.get(f"{base_url}/")
    assert unique_plate not in verify.text
