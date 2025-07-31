import obd
import datetime

connection = obd.OBD("/dev/ttyUSB0")

if connection.is_connected():
    print("✅ Connected to OBD-II adapter.")
else:
    print("❌ Failed to connect to OBD-II adapter. Exiting.")
    exit()

# ----- Live sensor readings ----- #

commands = {
    "RPM": obd.commands.RPM,
    "Speed": obd.commands.SPEED,
    "Throttle Position": obd.commands.THROTTLE_POS,
    "Engine Load": obd.commands.ENGINE_LOAD,
    "Coolant Temperature": obd.commands.COOLANT_TEMP,
    "Fuel Level": obd.commands.FUEL_LEVEL,
    "Intake Air Temperature": obd.commands.INTAKE_TEMP,
}

timestamp =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("obd_data.csv", "a") as f:
    f.write(f"Timestamp: {timestamp}\n")
    for name, cmd in commands.items():
        response = connection.query(cmd)
        if response.is_null():
            print(f"{name}: Not supported")
            f.write(f"{timestamp},{name},\n")
        else:
            print(f"{name}: {response.value}")
            f.write(f"{timestamp},{name},{response.value}\n")


# ----- DTC scanning ----- #

dtc_response = connection.query(obd.commands.GET_DTC)

with open("dtc_codes.csv", "a") as dtc_file:
    dtc_file.write(f"Timestamp: {timestamp}\n")
    if dtc_response.value and len(dtc_response.value) > 0:
        print("❗ Trouble codes found:\n")
        for code, desc in dtc_response.value:
            print(f" - Code: {code}")
            print(f"   Meaning: {desc}\n")
            dtc_file.write(f"{timestamp},{code},{desc}\n")
    else:
        print("✅ No trouble codes found.")
        dtc_file.write(f"{timestamp},No trouble codes found\n")

connection.close()
print("🔌 Connection closed.")

