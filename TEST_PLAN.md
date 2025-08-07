# Test Plan – Parking Lot Manager

## 1. Purpose & Scope

Test the main features of the Parking Lot Manager web application, running locally via Docker.  
Focus is on core API and web UI workflows, covering both positive and negative scenarios.

---

## 2. Test Objectives

- Check parking flow (start/end parking)  
- Validate input fields (car plate, slot)  
- Test user management (add/delete)  
- Ensure login/logout works  
- Test error handling and messages  

---

## 3. Assumptions & Risks

- Desktop browser only (Chrome)  
- No backend/API documentation available (API endpoints reverse-engineered using browser DevTools)  
- Test data and environment reset between runs may be required to avoid state conflicts  
- Authentication is required for all flows  
- All tests are run locally; no mobile  

---

## 4. Test Strategy

**Automation-first:**  
Core business flows (authentication, parking logic, error scenarios) are automated.

**Manual:**  
Used for exploratory UI flows, edge cases, and validating unexpected behaviors during new feature rollout.

**Framework is modular:**  
Easy to extend for additional backend or UI tests with minimal manual intervention.

---

## 5. Environment

- Docker Image: `doringber/parking-manager:3.1.0`  
- Test URL: `http://localhost:5000`  
- Browser: Google Chrome  
- Credentials: Provided securely (`admin` / `password` and alternates via `.env` file)  
- Test Data Reset: Recommend restarting the Docker container for a clean state if issues are encountered  

---

## 6. Test Data Examples

- Valid plates: `12345679`, `87654320`  
- Invalid plates: `1234`, `ABCDEFGH` *(not possible to fill – which is good)*  
- Slots: `1`, `999`  
- Usernames: `admin`, `tester`  

---

## 7. Test Cases

📝 [Full Test Suite – Google Sheet](https://docs.google.com/spreadsheets/d/1NL6RhU7bshcOqsH3w6sQaGhJYqcHWXhCvfm5W8vFSU0/edit?gid=0#gid=0)

---

## 8. Automation Scope

The automation suite covers the following core areas:

- **User Login**  
  Automated login for multiple user accounts (admin and secondary user), validating authentication and session handling.

- **Start Parking Workflow**  
  Starting a parking session for a unique car plate, with required field validation.  
  *(API and UI)*

- **Duplicate Parking Prevention (Same User)**  
  Preventing the same user from starting multiple parking sessions for the same car plate.  
  *(API)*

- **Duplicate Parking Prevention (Different Users)**  
  Preventing different users from parking the same car simultaneously, including validation of the UI notification for duplicate attempts.  
  *(API and UI)*

- **Multi-User Flows**  
  Sequential flows where User A performs an action (e.g., start parking), and User B interacts afterward.  
  *(UI)*

### Test Table Overview

#### API Tests

| ID  | Description                                 |
| --- | ------------------------------------------- |
| TC1 | Start parking with valid data               |
| TC2 | Duplicate start parking from same user      |
| TC3 | Duplicate start parking from different user |

#### UI Tests

| ID  | Description                                 |
| --- | ------------------------------------------- |
| TC3 | Duplicate start parking, different user (UI) |

🧪 Each test runs independently with unique license plates (except the UI test, which uses a fixed plate) and authenticates via user credentials from `.env`.

---

## 9. Out of Scope

- Mobile browser and device testing  
- Performance, load, or security testing  
- Database-level testing or direct DB access  
- End-to-end email/SMS notifications  
- 3rd-party integrations, if any  

---

## 10. Bug Reports

🐞 [Bug Tracker – Google Sheet](https://docs.google.com/spreadsheets/d/1sbHxLz2ShVLxnYpsxOpBt9_Z_ub8HoOJHIShRjY1g1I/edit?gid=0#gid=0)

---

## 11. Improvement Suggestions

- **Input Validation**  
  Add input masks for car plates and slot fields to prevent invalid data entry.

- **Active Parking Sessions Tab**  
  Add a dedicated "Active Parking" tab for immediate user feedback and better real-time monitoring.  
  **User:** Clear visibility that parking has started.  
  **System:** Real-time updates; separate active from historical records.

- **Test Data Reset Utility**  
  Consider adding an API or UI feature to reset test data between runs for consistent automation results.