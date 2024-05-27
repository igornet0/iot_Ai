from logger import SQLighter
from models import *
import time 

client_db = SQLighter("db.db")
#client_db.add_user("Test")
user = client_db.get_user("Test")
user = User(user[1], client_db)

# dv1 = Bulb("Кухня")
# dv2 = Socket("Кухня")
# dv3 = Socket("Спальня")
# dv4 = Bulb("Спальня")
# dv5 = Kettle("1")
# dv6 = Thermometer("Улица")
# dv7 = Kettle("2")

# user.add_device_db(dv1)
# user.add_device_db(dv2)
# user.add_device_db(dv3)
# user.add_device_db(dv4)
# user.add_device_db(dv5)
# user.add_device_db(dv6)
# user.add_device_db(dv7)


log_devices = client_db.get_log_devices()
log_sensors = client_db.get_log_sensors()

max_s = {}
min_s = {}
avg_s = {}

s = {}
for id, sensorid, value in log_sensors:

    value = int(value.split()[0])
    s[sensorid] = s.setdefault(sensorid, 0) + 1
    avg_s[sensorid] = avg_s.setdefault(sensorid, 0) + value
    max_s[sensorid] = max(max_s.setdefault(sensorid, 0), value)
    min_s[sensorid] = min(min_s.setdefault(sensorid, 10000), value)

for key, item in avg_s.items():
    avg_s[key] = round(avg_s[key] / s[key], 2)

diveces = user.get_devices()
for device in diveces:
    print(device)
    for sensor in device.get_sensors():
        sensorid = sensor.get_id()
        print(f"{sensor.name}:")
        print(f"\tмаксимальное значение: ", max_s[sensorid])
        print(f"\tcреднее значение: ", avg_s[sensorid])
        print(f"\tминимальное значение: ", min_s[sensorid])
    print()
# print(s)
# print(max_s)
# print(avg_s)
