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
- **PID Discovery**: Find supported OBD-II PIDs for your vehicle
- **Diagnostic Trouble Codes**: Automatically reads and logs DTCs
- **CSV Export**: All data saved with timestamps for analysis
- **Docker Support**: Containerized deployment option
- **Graceful Error Handling**: Clean exit when vehicle connection is unavailable

## Project Structure

```
obd_project/
├── obd_data_logger.py    # Main data logging script
├── obd_pid_finder.py     # PID discovery utility
├── data/                 # Data storage directory
├── obd_data.csv          # Live sensor readings output
├── dtc_codes.csv         # Diagnostic trouble codes output
├── tests/                # Test suite
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── LICENSE               # License information
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## Requirements

- **Python**: 3.12+ (tested with 3.12.3)
- **Hardware**: USB ELM327 OBD-II adapter
- **Dependencies**: Listed in `requirements.txt`

## Installation

### Standard Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:AlexLangan/obd_project.git
   cd obd_project
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Docker Installation

Build and run using Docker:
```bash
docker build -t obd-logger .
docker run --device=/dev/ttyUSB0 -v $(pwd)/data:/app/data obd-logger
```

## Usage

### Data Logging

1. **Connect your OBD-II adapter** to your vehicle's diagnostic port and your computer's USB port

2. **Start the engine** (required for data transmission)

3. **Run the data logger**:
   ```bash
   python obd_data_logger.py
   ```

4. **View the data**: Check the generated CSV files:
   - `obd_data.csv` - Contains timestamped sensor readings
   - `dtc_codes.csv` - Contains any diagnostic trouble codes

### PID Discovery

To find out which PIDs your vehicle supports:
```bash
python obd_pid_finder.py
```

This will scan your vehicle and display all available OBD-II parameters.

## Output Format

### obd_data.csv
| Timestamp | RPM | Speed | Throttle | Engine Load | Coolant Temp | Fuel Level | Intake Temp |
|-----------|-----|-------|----------|-------------|--------------|------------|-------------|
| 2025-09-30 14:23:01 | 850 | 0 | 15.3 | 23.5 | 89 | 75.2 | 28 |

### dtc_codes.csv
| Timestamp | Code | Description |
|-----------|------|-------------|
| 2025-09-30 14:23:01 | P0420 | Catalyst System Efficiency Below Threshold |

## Testing

Run the test suite:
```bash
pytest tests/
```

## Troubleshooting

- **No connection**: Ensure the OBD-II adapter is properly connected and the ignition is on
- **Permission errors**: On Linux/Mac, you may need to add your user to the `dialout` group:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
  Then log out and back in for changes to take effect
- **Import errors**: Verify dependencies are installed: `pip install -r requirements.txt`
- **USB device not found**: Check the device path (usually `/dev/ttyUSB0` on Linux, `COM3` on Windows)

## Compatibility

This project uses the ELM327 protocol, which is compatible with most vehicles manufactured after 1996 (OBD-II compliant). However, available parameters may vary by make and model.

Use the `obd_pid_finder.py` utility to discover which parameters your specific vehicle supports.

## Development

### Virtual Environments

The project includes two virtual environment directories (both git-ignored):
- `venv/` - Standard virtual environment
- `obd-env/` - Alternative environment setup

Use whichever suits your workflow.

## License

See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

## Acknowledgments

- Built with [python-OBD](https://github.com/brendan-w/python-OBD) by Brendan Whitfield
- Compatible with most OBD-II compliant vehicles
