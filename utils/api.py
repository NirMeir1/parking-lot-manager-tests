"""Utility functions for interacting with the Parking Lot Manager API."""

from __future__ import annotations

from typing import Optional

import requests
from bs4 import BeautifulSoup


def login(session: requests.Session, base_url: str, username: str, password: str) -> requests.Response:
    """Log in to the application using provided credentials."""
    response = session.post(
        f"{base_url}/login",
        data={"username": username, "password": password},
        allow_redirects=True,
    )
    response.raise_for_status()
    return response


def get_csrf_token(session: requests.Session, base_url: str, path: str = "/") -> Optional[str]:
    """Fetch the CSRF token from a GET-accessible page."""
    response = session.get(f"{base_url}{path}")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find("input", {"name": "csrf_token"})
    return token["value"] if token else None


def start_parking(
    session: requests.Session,
    base_url: str,
    plate: str,
    slot: str = "A1",
    vehicle_type_id: int = 1,
) -> requests.Response:
    """Start parking for a given vehicle plate."""
    start_url = f"{base_url}/start"
    token = get_csrf_token(session, base_url)
    files = {"image": ("dummy.jpg", b"dummy", "image/jpeg")}
    data = {
        "csrf_token": token,
        "car_plate": plate,
        "vehicle_type_id": vehicle_type_id,
        "slot": slot,
        "submit": "Start",
    }

    return session.post(start_url, data=data, files=files, allow_redirects=True)


def find_parking_id(html: str, plate: str) -> Optional[str]:
    """Locate a parking session ID from the active list HTML for the given plate."""
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.select("tr"):
        if plate in row.get_text():
            link = row.find("a", href=lambda x: x and x.startswith("/end/"))
            if link:
                return link["href"].rstrip("/").split("/")[-1]
    return None


def count_plate_occurrences(html: str, plate: str) -> int:
    """Count how many times a plate appears in the active parking table."""
    soup = BeautifulSoup(html, "html.parser")
    return sum(1 for row in soup.select("tr") if plate in row.get_text())


def end_parking(session: requests.Session, base_url: str, parking_id: str) -> requests.Response:
    """End parking session by ID."""
    url = f"{base_url}/end/{parking_id}"
    token = get_csrf_token(session, base_url)
    data = {"csrf_token": token, "submit": "End"}
    return session.post(url, data=data, allow_redirects=True)
