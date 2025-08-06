"""Shared pytest fixtures."""

import os
import pytest
import requests
from dotenv import load_dotenv

from utils import api
from utils.generator import random_plate


@pytest.fixture(scope="session")
def config():
    """Load configuration from environment variables."""
    load_dotenv()
    return {
        "base_url": os.getenv("BASE_URL", "http://localhost:5000"),
        "username": os.getenv("USERNAME", "admin"),
        "password": os.getenv("PASSWORD", "password"),
        "alt_username": os.getenv("ALT_USERNAME"),
        "alt_password": os.getenv("ALT_PASSWORD"),
    }


@pytest.fixture(scope="session")
def base_url(config):
    return config["base_url"]


@pytest.fixture
def session(config):
    session = requests.Session()
    api.login(session, config["base_url"], config["username"], config["password"])
    return session


@pytest.fixture
def alt_session(config):
    if not config.get("alt_username") or not config.get("alt_password"):
        pytest.skip("ALT user credentials not provided")
    session = requests.Session()
    api.login(session, config["base_url"], config["alt_username"], config["alt_password"])
    return session


@pytest.fixture
def unique_plate():
    return random_plate()
