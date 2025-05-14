[//]: # (cd to the project)

# Playwright Automation Test Project

This is an end-to-end automation testing project using **Playwright**, **Pytest**, **Docker**, and **Allure**
reporting.  
It supports both **local execution** with virtual environments and **Dockerized test runs**.

---

## 📂 Project Structure

.
├── src/
│ ├── helpers/
│ ├── page_objects/
│ ├── tests/
│ │ ├── data/
│ │ ├── conftest.py
│ │ └── test_airbnb_booking_flow.py
├── requirements.txt
├── setup.py
├── Dockerfile
├── run_tests.sh
└── README.md

---

## Requirements

To run this project locally or via Docker, ensure the following are installed:

- Python 3.9+
- Docker (for container-based execution)
- Bash (for running scripts)

---

## Installation & Setup

### Make the script executable

Before running anything, grant execution permissions:

```bash
chmod +x run_tests.sh
```

### Option 1: Local Installation

You can install and run the project locally using a virtual environment.

#### Step 1 – Install locally with venv:

```bash
./run_tests.sh --install-local --with-venv
source venv/bin/activate
```

#### Step 2 – Run tests locally:

```bash
pytest --base-url=https://airbnb.com --headed
```

#### Optional

You may also use --no-venv if running in an already activated environment:

```bash
./run_tests.sh --install-local --no-venv
```

### Option 2: Using Docker

#### Build Docker No cache

```bash
./run_tests.sh --docker-build
```

#### Option 2: Using Docker

```bash
./run_tests.sh --docker-run --base-url=https://airbnb.com
```
