# 🏙️ Smart City CI/CD Pipeline

> **Automated testing & Continuous Integration for Smart City metric calculations.**  
> Every push triggers a GitHub Actions pipeline that runs 15 unit tests across Python 3.10, 3.11, and 3.12 — catching bugs before they reach production.
---

## 🔍 Overview

This project demonstrates **Continuous Integration (CI)** principles applied to a Smart City software system. It simulates the kind of automated quality assurance pipelines used in real-world cloud infrastructure and DevOps environments.

The system:
- Implements **3 Python functions** that calculate Smart City metrics
- Validates them with **15 unit tests** using Python's built-in `unittest` framework
- Automates test execution via **GitHub Actions** on every code push
- Tests across **3 Python versions** (3.10, 3.11, 3.12) in parallel

The goal is simple: **catch bugs automatically, before they cause problems.**

---

## 🤖 What is CI/CD?

**Continuous Integration (CI)** means every time a developer pushes code, an automated system immediately runs tests to verify nothing is broken.

Think of it as a robot colleague who checks your work the instant you submit it — before it reaches users.

```
Developer pushes code
        ↓
GitHub detects the push
        ↓
GitHub Actions spins up a virtual machine
        ↓
Installs Python & runs all 15 tests
        ↓
✅ Green = safe to merge   ❌ Red = bug detected, fix required
```

---

## 📁 Project Structure

```
smart-city-cicd/
│
├── smart_city.py            # Core Smart City calculation functions
├── test_smart_city.py       # 15 unit tests (3 classes × 5 tests)
├── README.md                # This file
│
└── .github/
    └── workflows/
        └── ci.yml           # GitHub Actions CI pipeline config
```

---

## 🏙️ Smart City Functions

All functions are in `smart_city.py`. They are **pure functions** — no side effects, no global state, deterministic output.

### 1. `calculate_energy_efficiency`

Calculates energy consumption per capita for a city zone.

```python
def calculate_energy_efficiency(consumption_kwh, population):
    """
    Returns: float — kWh per person (rounded to 2dp)
    Raises:  ValueError if population <= 0
    """
```

| Input | Example | Output |
|---|---|---|
| `consumption_kwh=50000, population=1000` | Normal zone | `50.0` kWh/person |
| `consumption_kwh=100, population=3` | Small zone | `33.33` kWh/person |
| `population=0` | Invalid | `ValueError` |

---

### 2. `calculate_traffic_congestion_index`

Calculates a congestion ratio for a road segment. Values above `1.0` indicate gridlock.

```python
def calculate_traffic_congestion_index(vehicles, road_capacity):
    """
    Returns: float — vehicles/capacity ratio (rounded to 2dp)
    Raises:  ValueError if road_capacity <= 0
    """
```

| Index Value | Meaning |
|---|---|
| `0.0` | Empty road |
| `0.1 – 0.7` | Light traffic |
| `0.8 – 0.9` | Moderate traffic |
| `1.0` | At full capacity |
| `> 1.0` | 🚨 Gridlock — over capacity |

---

### 3. `calculate_air_quality_index`

Calculates a composite Air Quality Index (AQI) score from three pollution inputs.

```python
def calculate_air_quality_index(pm25, pm10, no2):
    """
    Returns: dict — { "score": float, "category": str }
    Raises:  ValueError if any value < 0
    Formula: score = (pm25 × 0.5) + (pm10 × 0.3) + (no2 × 0.2)
    """
```

| Score Range | Health Category |
|---|---|
| `0 – 50` | ✅ Good |
| `51 – 100` | 🟡 Moderate |
| `101 – 150` | 🟠 Unhealthy for Sensitive Groups |
| `> 150` | 🔴 Unhealthy |

---

## 🧪 Unit Tests

Tests are in `test_smart_city.py` using Python's `unittest` framework.

**15 tests across 3 test classes:**

| Test Class | Tests | Covers |
|---|---|---|
| `TestEnergyEfficiency` | 5 | Normal calc, small city, rounding, zero population, negative population |
| `TestTrafficCongestion` | 5 | Light traffic, full capacity, gridlock, empty road, zero capacity |
| `TestAirQualityIndex` | 5 | Good air, moderate air, dict keys, negative values, zero pollution |

**Assertion methods used:**

```python
self.assertEqual()       # Verifies exact return value
self.assertRaises()      # Verifies ValueError is raised on bad input
self.assertLessEqual()   # Verifies score is within expected range
self.assertIn()          # Verifies dict contains required keys
```

---

## ⚙️ GitHub Actions Workflow

The CI pipeline is defined in `.github/workflows/ci.yml`.

```yaml
name: Smart City CI

on:
  push:
    branches: [ "**" ]       # Run on every push to any branch
  pull_request:
    branches: [ "main" ]     # Run on PRs targeting main

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]   # 3 parallel jobs

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m unittest test_smart_city.py -v
```

**What happens on every push:**

```
Push detected
    ↓
3 parallel jobs spin up (Python 3.10 / 3.11 / 3.12)
    ↓
Each job: checkout → install Python → run 15 tests
    ↓
All 3 must pass for ✅ green status
    ↓
Any failure → ❌ red status + developer notified
```

---

## 🖥️ Running Tests Locally

**Prerequisites:** Python 3.10 or higher, Git

```bash
# 1. Clone the repository
git clone https://github.com/shuhaibabdulla/smart-city-cicd.git
cd smart-city-cicd

# 2. Run all tests with verbose output
python -m unittest test_smart_city.py -v

# 3. Or use discovery mode (finds all test_*.py files)
python -m unittest discover -v
```

**Expected output:**

```
test_full_capacity (test_smart_city.TestTrafficCongestion) ... ok
test_light_traffic (test_smart_city.TestTrafficCongestion) ... ok
test_over_capacity_gridlock (test_smart_city.TestTrafficCongestion) ... ok
test_empty_road (test_smart_city.TestTrafficCongestion) ... ok
test_zero_capacity_raises_error (test_smart_city.TestTrafficCongestion) ... ok
test_normal_calculation (test_smart_city.TestEnergyEfficiency) ... ok
test_small_city (test_smart_city.TestEnergyEfficiency) ... ok
test_rounding (test_smart_city.TestEnergyEfficiency) ... ok
test_zero_population_raises_error (test_smart_city.TestEnergyEfficiency) ... ok
test_negative_population_raises_error (test_smart_city.TestEnergyEfficiency) ... ok
test_good_air_quality (test_smart_city.TestAirQualityIndex) ... ok
test_moderate_air_quality (test_smart_city.TestAirQualityIndex) ... ok
test_returns_dict_with_correct_keys (test_smart_city.TestAirQualityIndex) ... ok
test_negative_values_raise_error (test_smart_city.TestAirQualityIndex) ... ok
test_zero_pollution_is_good (test_smart_city.TestAirQualityIndex) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.003s

OK
```

---

## 🔄 CI Pipeline in Action

### ✅ When all tests pass:

```
Smart City CI
  ├── test (3.10)  ✅  ~18s
  ├── test (3.11)  ✅  ~16s
  └── test (3.12)  ✅  ~17s

15 tests · 0 failures · 0 errors · 3 Python versions
```

### ❌ When a bug is introduced:

```
Smart City CI
  ├── test (3.10)  ❌  FAILED
  │     AssertionError: 50000000.0 != 50.0
  │     (bug: used * instead of / in energy calculation)
  ├── test (3.11)  ❌  FAILED
  └── test (3.12)  ❌  FAILED

→ Developer reads the log, fixes the bug, pushes again → ✅
```

This is CI/CD working exactly as designed.

---

## 📊 Sample Output

```python
from smart_city import (
    calculate_energy_efficiency,
    calculate_traffic_congestion_index,
    calculate_air_quality_index
)

# Energy efficiency
print(calculate_energy_efficiency(50000, 1000))
# Output: 50.0

# Traffic congestion
print(calculate_traffic_congestion_index(1200, 1000))
# Output: 1.2  ← gridlock!

# Air quality
print(calculate_air_quality_index(10, 20, 15))
# Output: {'score': 14.0, 'category': 'Good'}
```

## 📋 Academic Context

| Detail | Info |
|---|---|
| **University** | Yenepoya Deemed to be University |
| **Program** | BCA (AI, Cloud Computing & DevOps) with IBM & TCS |
| **Semester** | VI Semester — Third Year |
| **Academic Year** | 2025–2026 |
| **Subject** | Artificial Intelligence, Cloud Computing and DevOps |
| **Project Type** | Automated Testing & CI/CD Pipeline |
| **Tools Used** | Python, unittest, GitHub Actions |
| **Theme** | Smart City CI/CD Pipeline Automation |
---

## 👤 Author

**Suzana Sehanaz**  
BCA (AI, Cloud Computing & DevOps) with IBM & TCS — VI Semester  
Yenepoya Deemed to be University  
GitHub: 

---

## 📄 License

This project is submitted for academic purposes at Yenepoya Deemed to be University. All Smart City metrics and data used are simulated and do not represent any real city infrastructure or live sensor data.

---
