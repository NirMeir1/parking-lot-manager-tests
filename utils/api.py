"""Helpers for talking to the Parking-Lot-Manager HTTP interface."""

from __future__ import annotations

from typing import Optional

import requests
from bs4 import BeautifulSoup


# ──────────────────────────────  AUTH  ──────────────────────────────────


def login(
    session: requests.Session,
    base_url: str,
    username: str,
    password: str,
) -> requests.Response:
    """
    Perform a CSRF-protected login *and* fail loudly when authentication
    does not succeed (wrong creds / missing token, …).
    """
    token = (
        get_csrf_token(session, base_url, "/login")
        or get_csrf_token(session, base_url, "/")
    )
    if token is None:
        raise RuntimeError("Could not extract CSRF token from login page")

    resp = session.post(
        f"{base_url}/login",
        data={
            "username": username,
            "password": password,
            "csrf_token": token,
        },
        allow_redirects=True,
    )

    # ── sanity-checks ────────────────────────────────────────────────
    if resp.url.endswith("/login"):
        raise RuntimeError("Login failed – server kept us on /login")
    if not session.cookies.get_dict():
        raise RuntimeError("Login failed – no session cookie set")
    # ────────────────────────────────────────────────────────────────

    return resp


def get_csrf_token(
    session: requests.Session,
    base_url: str,
    path: str = "/",
) -> Optional[str]:
    """
    Return the CSRF token rendered in *path*.

    Looks for an ``<input>`` whose **name OR id** equals ``csrf_token``.
    """
    resp = session.get(f"{base_url}{path}", allow_redirects=True)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    token_input = (
        soup.find("input", attrs={"name": "csrf_token"})
        or soup.find("input", attrs={"id": "csrf_token"})
    )
    return token_input["value"] if token_input else None


# ────────────────────────  PARKING ENDPOINTS  ──────────────────────────


def start_parking(
    session: requests.Session,
    base_url: str,
    plate: str,
    slot: str = "A1",
    vehicle_type_id: int = 1,
) -> requests.Response:
    """Open a new parking session for *plate*."""
    token = get_csrf_token(session, base_url, "/")
    files = {"image": ("dummy.jpg", b"dummy", "image/jpeg")}
    data = {
        "csrf_token": token,
        "car_plate": plate,
        "vehicle_type_id": vehicle_type_id,
        "slot": slot,
        "submit": "Start",
    }
    return session.post(f"{base_url}/start", data=data, files=files, allow_redirects=True)


def end_parking(
    session: requests.Session,
    base_url: str,
    parking_id: str,
) -> requests.Response:
    """Close an active parking session by *parking_id*."""
    token = get_csrf_token(session, base_url, "/")
    data = {"csrf_token": token, "submit": "End"}
    return session.post(f"{base_url}/end/{parking_id}", data=data, allow_redirects=True)


# ───────────────────────────────  HTML UTILS  ──────────────────────────


def find_parking_id(html: str, plate: str) -> Optional[str]:
    """Return the /end/<id> for *plate* from dashboard HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.select("tr"):
        if plate in row.get_text():
            link = row.find("a", href=lambda h: h and h.startswith("/end/"))
            if link:
                return link["href"].rstrip("/").split("/")[-1]
    return None


def count_plate_occurrences(html: str, plate: str) -> int:
    """Count how many times *plate* appears in the active-parking table."""
    soup = BeautifulSoup(html, "html.parser")
    return sum(1 for row in soup.select("tr") if plate in row.get_text())