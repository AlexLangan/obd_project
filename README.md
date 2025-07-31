# OBD-II Data Logger

This Python script connects to a USB OBD-II adapter and reads live car data and trouble codes. Tested on a **2015 Ford Fiesta Diesel**.

## ✅ Features

- Logs key engine sensor data:
  - RPM  
  - Speed  
  - Throttle Position  
  - Engine Load  
  - Coolant Temperature  
  - Fuel Level  
  - Intake Air Temperature  
- Reads Diagnostic Trouble Codes (DTCs)
- Adds timestamps to all data
- Saves results to CSV files
- Cleanly exits if the car is not connected

## 📁 Files

| File                   | Description                          |
|------------------------|--------------------------------------|
| `0bd_test_real.py`     | Main script for logging data         |
| `obd_data.csv`         | Stores live sensor readings          |
| `dtc_codes.csv`        | Stores trouble codes  |
| `.gitignore`           | Hides CSV files and virtual env      |

## 🔧 Requirements

- Python 3.x  
- USB ELM327 OBD-II adapter  
- [python-OBD library](https://github.com/brendan-w/python-OBD)

## ⚙️ Setup

1. Clone repository:
```bash
git clone git@github.com:AlexLangan/0bd_test_real.git
cd 0bd_test_real
```