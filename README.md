# parking-lot-manager-tests

Automated test suite for the **Pango Pay & Go – Parking Lot Manager**.
API tests use `pytest`, `requests`, and `python-dotenv` while a single UI
scenario is covered with `pytest-playwright`.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables in `.env` (sample values are provided):
   ```env
   BASE_URL=http://localhost:5000
   USERNAME=will_be_provided_securely
   PASSWORD=will_be_provided_securely
   ALT_USERNAME=will_be_provided_securely
   ALT_PASSWORD=will_be_provided_securely
   ```

   Note: The credentials will be provided securely by the test author (via email or other private means). Please do not attempt to run the tests without updating the .env file.

## Running Tests
Ensure the Parking Lot Manager application is running locally. Install the
Playwright browsers once:
```bash
playwright install
```

Run the full test suite:
```bash
pytest
```

Run only the UI test:
```bash
pytest -m ui
```

## Documentation
The suite includes tests for starting parking sessions and preventing duplicate
parking attempts. See `TEST_PLAN.md` for a detailed description of coverage.