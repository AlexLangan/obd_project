#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import obd

load_dotenv()
OBD_PORT = os.getenv("OBD_PORT", "/dev/ttyUSB0")


def main():
    """
    Connects to the OBD-II adapter, queries all OBD-II commands,
    and prints supported PIDs and their values.
    """
    connection = obd.OBD(OBD_PORT)
    if not connection.is_connected():
        print("❌ Failed to connect to OBD-II adapter.")
        return

    print(f"✅ Connected to OBD-II adapter on {OBD_PORT}")
    print("Scanning supported PIDs...")

    for cmd_name in dir(obd.commands):
        if cmd_name.isupper():
            cmd = getattr(obd.commands, cmd_name)
            response = connection.query(cmd)
            if response.is_null():
                print(f"{cmd_name}: Not supported")
            else:
                print(f"{cmd_name}: Supported, Value: {response.value}")

    connection.close()
    print("🔌 Connection closed.")


if __name__ == "__main__":
    main()
