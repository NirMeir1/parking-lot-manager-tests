"""UI tests for parking-lot manager duplicate plate scenario."""

from __future__ import annotations

import os

from playwright.sync_api import Page, expect

PLATE = "82743904"
SLOT = "A1"
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


def login(page: Page, username: str, password: str) -> None:
    """Authenticate user via the login page."""
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#submit")
    expect(page.locator("#car_plate")).to_be_visible()


def start_parking(page: Page, plate: str, slot: str) -> None:
    """Start parking for a given plate and slot."""
    page.fill("#car_plate", plate)
    page.fill("#slot", slot)
    page.click("#submit")


def logout(page: Page) -> None:
    """Log out the current user."""
    page.click('a[href="/logout"]')


def test_tc3_start_parking_duplicate_plate_different_user(page: Page) -> None:
    """TC3 – Start Parking Duplicate Plate – Different User."""
    login(page, os.getenv("USERNAME"), os.getenv("PASSWORD"))
    start_parking(page, PLATE, SLOT)
    logout(page)

    login(page, os.getenv("ALT_USERNAME"), os.getenv("ALT_PASSWORD"))
    start_parking(page, PLATE, SLOT)

    toast = page.locator("div.alert.alert-warning.alert-dismissible.fade.show")
    expect(toast).to_have_text(
        "Duplicate parking prevented: this car is already parked."
    )

