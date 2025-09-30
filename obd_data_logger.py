#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import obd
import datetime
import csv
import sys
import time
import logging

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

# --- CSV Files (Docker-friendly / persistent) ---
OBD_FILE = "data/obd_data.csv"
DTC_FILE = "data/dtc_codes.csv"

# --- Ensure directories exist ---
os.makedirs(os.path.dirname(OBD_FILE), exist_ok=True)
os.makedirs(os.path.dirname(DTC_FILE), exist_ok=True)

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


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
            logging.warning(f"{name}: Not supported")
            row.append("")
        else:
            logging.info(f"{name}: {response.value}")
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
            logging.warning("❗ Trouble codes found:")
            for code, desc in dtc_response.value:
                logging.warning(f" - {code}: {desc}")
                writer.writerow([timestamp, code, desc])
        else:
            logging.info("✅ No trouble codes found.")
            writer.writerow([timestamp, "None", "No trouble codes"])


def main(interval=60):
    """Main loop for live logging with connection retries."""
    connection = None
    for attempt in range(5):  # Retry up to 5 times
        connection = obd.OBD(OBD_PORT)
        if connection.is_connected():
            logging.info(f"✅ Connected to OBD-II adapter on {OBD_PORT}")
            break
        logging.info("⏳ Waiting for OBD-II adapter...")
        time.sleep(3)
    else:
        logging.error("❌ Could not connect to OBD-II adapter. Exiting.")
        sys.exit(1)

    try:
        while True:
            log_sensors(connection)
            log_dtcs(connection)
            logging.info("-" * 40)
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("🛑 Logging stopped by user.")
    finally:
        connection.close()
        logging.info("🔌 Connection closed.")


if __name__ == "__main__":
    # Initialize CSVs with headers
    sensor_headers = ["Timestamp"] + list(COMMANDS.keys())
    init_csv(OBD_FILE, sensor_headers)
    init_csv(DTC_FILE, ["Timestamp", "Code", "Description"])

    # Start logging every 60 seconds
    main(interval=60)
