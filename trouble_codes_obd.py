import obd 

connection = obd.OBD("/dev/ttyUSB0") 

if not connection.is_connected():
    print("❌ Could not connect to the car.")
    exit() 

print("✅ Connected to the car.\n")

# Ask the car for stored Diagnostic Trouble Codes (DTCs)
dtc_response = connection.query(obd.commands.GET_DTC)

if dtc_response.value and len(dtc_response.value) > 0:
    print("❗ Trouble codes found:\n")
    for code, desc in dtc_response.value:
        print(f" - Code: {code}")
        print(f"   Meaning: {desc}\n")
else:
    print("✅ No trouble codes found.")

connection.close()
print("🔌 Connection closed.")
