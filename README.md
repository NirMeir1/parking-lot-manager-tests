# Parking Lot Manager Tests

Automated tests for the Parking Lot Manager app (API + UI).

## Prerequisites
- Python 3.10+
- Install Playwright browsers:
  ```bash
  playwright install --with-deps
  ```

## Environment Variables
Create a `.env` from the template:
```bash
cp .env.example .env
```
Update values if needed. **Do not commit `.env`.**

## Install Dependencies
```bash
pip install -r requirements.txt
```
This includes `pytest-xdist` for parallel execution.

## Running Tests
**API tests (parallel):**
```bash
pytest -m api -n auto -q
```

**UI tests (serial):**
```bash
pytest -m ui -n 1 -q
```

**All (API parallel, UI serial):**
```bash
pytest -m "api" -n auto -q && pytest -m "ui" -n 1 -q
```

## Notes
- Tests use namespaced data per worker to avoid collisions.
- Sessions are function-scoped to prevent state leakage.
