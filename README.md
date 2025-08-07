# parking-lot-manager-tests

Automated API test suite for the **Pango Pay & Go – Parking Lot Manager**.
The suite is built with `pytest`, `requests`, and `python-dotenv` and
covers core parking workflows.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables in `.env` (sample values are provided):
   ```env
   BASE_URL=http://localhost:5000
   USERNAME=admin
   PASSWORD=password
   ALT_USERNAME=blabla
   ALT_PASSWORD=12345
   ```

## Running Tests
Ensure the Parking Lot Manager application is running locally and then execute:
```bash
pytest
```

The suite includes tests for starting and ending parking sessions, as well as
checks for preventing duplicate parking attempts.
