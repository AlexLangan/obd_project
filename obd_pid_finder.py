import obd

connection = obd.OBD("/dev/ttyUSB0")

if not connection.is_connected():
    print("Failed to connect to OBD-II adapter.")
    exit()

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
print("Connection closed.")
