# OBD-II Data Logger

A Python-based diagnostic tool for reading and logging live vehicle data through a USB OBD-II adapter. This project enables real-time monitoring of engine parameters and retrieval of diagnostic trouble codes (DTCs).

## Features

- **Live Sensor Monitoring**: Continuously logs key engine metrics
  - Engine RPM
  - Vehicle Speed
  - Throttle Position
  - Engine Load Percentage
  - Coolant Temperature
  - Fuel Level
  - Intake Air Temperature
- **Diagnostic Trouble Codes**: Automatically reads and logs DTCs
- **CSV Export**: All data saved with timestamps for analysis
- **Graceful Error Handling**: Clean exit when vehicle connection is unavailable
- **Tested Hardware**: Validated on 2015 Ford Fiesta Diesel

## Project Structure

```
obd_project/
├── 0bd_test_real.py    # Main data logging script
├── obd_data.csv        # Live sensor readings output
├── dtc_codes.csv       # Diagnostic trouble codes output
├── .gitignore          # Excludes CSV files and virtual environment
└── README.md           # Project documentation
```

## Requirements

- **Python**: 3.x or higher
- **Hardware**: USB ELM327 OBD-II adapter
- **Library**: [python-OBD](https://github.com/brendan-w/python-OBD)

## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:AlexLangan/obd_project.git
   cd obd_project
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install obd
   ```

## Usage

1. **Connect your OBD-II adapter** to your vehicle's diagnostic port and your computer's USB port

2. **Start the engine** (required for data transmission)

3. **Run the script**:
   ```bash
   python 0bd_test_real.py
   ```

4. **View the data**: Check the generated CSV files:
   - `obd_data.csv` - Contains timestamped sensor readings
   - `dtc_codes.csv` - Contains any diagnostic trouble codes

## Output Format

### obd_data.csv
| Timestamp | RPM | Speed | Throttle | Engine Load | Coolant Temp | Fuel Level | Intake Temp |
|-----------|-----|-------|----------|-------------|--------------|------------|-------------|
| 2025-09-30 14:23:01 | 850 | 0 | 15.3 | 23.5 | 89 | 75.2 | 28 |

### dtc_codes.csv
| Timestamp | Code | Description |
|-----------|------|-------------|
| 2025-09-30 14:23:01 | P0420 | Catalyst System Efficiency Below Threshold |

## Troubleshooting

- **No connection**: Ensure the OBD-II adapter is properly connected and the ignition is on
- **Permission errors**: On Linux/Mac, you may need to add your user to the `dialout` group or run with `sudo`
- **Import errors**: Verify python-OBD is installed: `pip list | grep obd`

## Compatibility

This project uses the ELM327 protocol, which is compatible with most vehicles manufactured after 1996 (OBD-II compliant). However, available parameters may vary by make and model.

## License

This project is open source and available for personal and educational use.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

## Acknowledgments

- Built with [python-OBD](https://github.com/brendan-w/python-OBD) by Brendan Whitfield
- Tested on Ford vehicles but should work with most OBD-II compliant cars
