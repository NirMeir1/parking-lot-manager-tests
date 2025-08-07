"""Tests for ending parking sessions."""

from utils.api import start_parking, end_parking, find_parking_id, count_plate_occurrences


def test_tc18_end_parking_valid(session, base_url, unique_plate):
    """TC18 – End Parking (Valid)."""
    start_parking(session, base_url, unique_plate)
    dashboard = session.get(f"{base_url}/")
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1
    parking_id = find_parking_id(dashboard.text, unique_plate)
    assert parking_id is not None

    response = end_parking(session, base_url, parking_id)
    assert response.status_code == 200

    verify = session.get(f"{base_url}/")
    # TODO: replace HTML scraping with GET /api/parkings once available
    assert count_plate_occurrences(verify.text, unique_plate) == 0
