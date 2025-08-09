from __future__ import annotations

import os
from typing import Dict

import pytest
import requests
from dotenv import load_dotenv

from utils import api
from utils.generator import random_plate

# ────────────────────────────────  CONFIG  ─────────────────────────────


@pytest.fixture(scope="session")
def config() -> Dict[str, str]:
    """Read connection / credential details from .env (override system)."""
    load_dotenv(override=True)
    return {
        "base_url":     os.getenv("BASE_URL", "http://localhost:5000"),
        "username":     os.getenv("USERNAME", "admin"),
        "password":     os.getenv("PASSWORD", "password"),
        "alt_username": os.getenv("ALT_USERNAME"),
        "alt_password": os.getenv("ALT_PASSWORD"),
    }


@pytest.fixture(scope="session")
def base_url(config):
    return config["base_url"]


# ───────────────────────────────  SESSIONS  ────────────────────────────


@pytest.fixture
def session(config):
    """Primary authenticated session (admin by default)."""
    s = requests.Session()
    try:
        api.login(s, config["base_url"], config["username"], config["password"])
        yield s
    except Exception as exc:
        pytest.fail(f"Auth failed in session fixture: {exc}")
    finally:
        s.close()


@pytest.fixture
def alt_session(config):
    """Alternative user session, skipped if creds not supplied."""
    if not (config.get("alt_username") and config.get("alt_password")):
        pytest.skip("ALT user credentials not provided")

    s = requests.Session()
    try:
        api.login(
            s,
            config["base_url"],
            config["alt_username"],
            config["alt_password"],
        )
        yield s
    except Exception as exc:
        pytest.fail(f"Auth failed in alt_session fixture: {exc}")
    finally:
        s.close()


# ──────────────────────────────  GENERATORS  ───────────────────────────


@pytest.fixture(scope="session")
def worker_namespace(worker_id: str) -> str:
    """Namespace for xdist workers; 'master' when not parallel."""
    return worker_id if worker_id != "master" else "gw0"

@pytest.fixture
def unique_plate(worker_namespace: str):
    """Random plate, namespaced per worker to avoid collisions."""
    return f"{worker_namespace}-{random_plate()}"
