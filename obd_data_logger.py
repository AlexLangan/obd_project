#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import obd
import datetime
import csv
import sys
import time

# --- Load environment variables ---
load_dotenv()
OBD_PORT = os.getenv("OBD_PORT", "/dev/ttyUSB0")

# --- OBD Commands ---
COMMANDS = {
    "RPM": obd.commands.RPM,
    "Speed": obd.commands.SPEED,
    "Throttle Position": obd.commands.THROTTLE_POS,
    "Engine Load": obd.commands.ENGINE_LOAD,
    "Coolant Temperature": obd.commands.COOLANT_TEMP,
    "Fuel Level": obd.commands.FUEL_LEVEL,
    "Intake Air Temperature": obd.commands.INTAKE_TEMP,
}

# --- CSV Files ---
OBD_FILE = "obd_data.csv"
DTC_FILE = "dtc_codes.csv"


def init_csv(file_path, headers):
    """Create CSV file with headers if it doesn't exist."""
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def log_sensors(connection):
    """Query all sensors and write a single row per timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp]

    for name, cmd in COMMANDS.items():
        response = connection.query(cmd)
        if response.is_null():
            print(f"{name}: Not supported")
            row.append("")
        else:
            print(f"{name}: {response.value}")
            row.append(str(response.value))

    with open(OBD_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def log_dtcs(connection):
    """Query DTC codes and write to CSV."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dtc_response = connection.query(obd.commands.GET_DTC)
    
    with open(DTC_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if dtc_response.value and len(dtc_response.value) > 0:
            print("❗ Trouble codes found:")
            for code, desc in dtc_response.value:
                print(f" - {code}: {desc}")
                writer.writerow([timestamp, code, desc])
        else:
            print("✅ No trouble codes found.")
            writer.writerow([timestamp, "None", "No trouble codes"])


def main(interval=2):
    """Main loop for live logging."""
    connection = obd.OBD(OBD_PORT)
    if not connection.is_connected():
        print("❌ Failed to connect to OBD-II adapter. Exiting.")
        sys.exit(1)
    print(f"✅ Connected to OBD-II adapter on {OBD_PORT}")

    try:
        while True:
            log_sensors(connection)
            log_dtcs(connection)
            print("-" * 40)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Logging stopped by user.")
    finally:
        connection.close()
        print("🔌 Connection closed.")


if __name__ == "__main__":
    # Initialize CSVs with headers
    sensor_headers = ["Timestamp"] + list(COMMANDS.keys())
    init_csv(OBD_FILE, sensor_headers)
    init_csv(DTC_FILE, ["Timestamp", "Code", "Description"])

    # Start logging
    main(interval=2)  # Log every 60 seconds instead of 2 for practical use. 
