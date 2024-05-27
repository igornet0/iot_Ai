from .devices import *

def get_device(device_type):
    if device_type == "Bulb":
        device = Bulb()
    elif device_type == "Thermostat":
        device = Thermostat()
    elif device_type == "Socket":
        device = Socket()
    elif device_type == "Kettle":
        device = Kettle()
    elif device_type == "Thermometer":
        device = Thermometer()
    elif device_type == "SensorMove":
        device = SensorMove()
    elif device_type == "Ventilation":
        device = Ventilation()
    elif device_type == "AirConditioner":
        device = AirConditioner()
    elif device_type == "Camera":
        device = Camera()
    elif device_type == "Lock":
        device = Lock()
    else:
        return None

    return device

class Api:

    def __init__(self, on=False, device_type="") -> None:
        self.on = on
        self.device = get_device(device_type)
        self.device_type = device_type

    def work_link(self):
        pass

    def work(self, sensors):
        if not self.on: 
            for sensor in sensors:
                work(self.device_type, sensor)
        for sensor in sensors:
            result = validate(self.device_type, sensor)
            if not result[0]:
                return result
        return True, None

    def validate(self, sensors):
        if self.on:
            for sensor in sensors:
                sensor.value = self.device.default_values[sensor.name]
                    
        return self.work(sensors)
        
