from __future__ import annotations

from typing import Dict

from playwright.sync_api import Page, expect
import pytest
pytestmark = pytest.mark.ui

PLATE: str = "82743904"      # 8-digit plate (no letters, non-sequential)
SLOT: str = "A1"             

# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def login(page: Page, base_url: str, username: str, password: str) -> None:
    """Log a user in and assert we reached the dashboard."""
    page.goto(f"{base_url}/login")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click('button[type="submit"]')              
    page.wait_for_url("**/")                         
    expect(page.locator("#car_plate")).to_be_visible()


def start_parking(page: Page, plate: str, slot: str) -> None:
    """Fill the dashboard form and start parking."""
    page.fill("#car_plate", plate)
    page.fill("#slot", slot)
    page.click("#submit")


def logout(page: Page) -> None:
    """Click the Logout link (top nav)."""
    page.click('a[href="/logout"]')
    page.wait_for_url("**/login")                    


# --------------------------------------------------------------------------- #
# Test case                                                                   #
# --------------------------------------------------------------------------- #
def test_tc3_start_parking_duplicate_plate_different_user(
    page: Page,
    config: Dict[str, str],
) -> None:
    """
    TC3 – Start Parking Duplicate Plate – Different User
    ----------------------------------------------------
    User-A parks PLATE → logout → User-B logs in → tries to park same PLATE
    Expect toast: “Duplicate parking prevented: this car is already parked.”
    """
    base_url   = config["base_url"]
    user_a     = config["username"]
    pass_a     = config["password"]
    user_b     = config["alt_username"]
    pass_b     = config["alt_password"]

    # ---------- User-A ----------
    login(page, base_url, user_a, pass_a)
    start_parking(page, PLATE, SLOT)
    logout(page)

    # ---------- User-B ----------
    login(page, base_url, user_b, pass_b)
    start_parking(page, PLATE, SLOT)

    # ---------- Verification ----------
    toast = page.locator("div.alert.alert-warning.alert-dismissible.fade.show")
    expect(toast).to_have_text(
        "Duplicate parking prevented: this car is already parked."
    )