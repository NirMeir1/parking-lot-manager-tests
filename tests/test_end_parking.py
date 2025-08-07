"""Tests related to *ending* an active parking session."""

import pytest

from utils.api import (
    start_parking,
    end_parking,
    find_parking_id,
    count_plate_occurrences,
)


@pytest.mark.usefixtures("session", "base_url", "unique_plate")
def test_tc18_end_parking_valid(session, base_url, unique_plate):
    """TC18 – End Parking (Valid)."""

    # ➊ Start a parking session
    start_parking(session, base_url, unique_plate)

    # ➋ Verify the plate is listed once
    dashboard = session.get(f"{base_url}/")
    assert count_plate_occurrences(dashboard.text, unique_plate) == 1

    # ➌ Resolve parking-ID and end the session
    parking_id = find_parking_id(dashboard.text, unique_plate)
    assert parking_id, "Could not extract parking ID from dashboard"

    resp = end_parking(session, base_url, parking_id)
    assert resp.status_code == 200

    # ➍ Ensure the plate is **gone**
    dashboard_after = session.get(f"{base_url}/")
    # TODO: Switch to /api/parkings endpoint once available
    assert count_plate_occurrences(dashboard_after.text, unique_plate) == 0