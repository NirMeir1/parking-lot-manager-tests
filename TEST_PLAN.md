# Test Plan

## API Tests

| ID  | Description                                   |
| --- | --------------------------------------------- |
| TC1 | Start parking with valid data                 |
| TC2 | Duplicate start parking from same user        |
| TC3 | Duplicate start parking from different user   |

## UI Tests

| ID  | Description                                   |
| --- | --------------------------------------------- |
| TC3 | Duplicate start parking, different user (UI)  |

Each test runs independently with unique license plates (except the UI test,
which uses a fixed plate) and authenticates via user credentials from `.env`.
