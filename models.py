from abc import ABC, abstractmethod
from random import randint
from logger import Client

diсt_RU = {"Bulb": "Лампочка", "Socket": "Розетка", "Kettle": "Чайник", "Thermometer": "Термометр"}

class Sensor:
    def __init__(self, name: str, unit: str, value: any = 0) -> None:
        self.name = name
        self.unit = unit
        self.value = value


    def get_value(self) -> any:
        return self.value
    

    def get_unit(self) -> str:
        return self.unit

    def set_value(self, item: any) -> any:
        self.value = item
        return self.get_value()


    def __str__(self) -> str:
        return f"{self.name} = {self.value}{self.unit}"


class Device(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self.name_device = diсt_RU[type(self).__name__]
        self.name_device_en = type(self).__name__
        self.sensors = []
        self.status_work = False
        self.status_connect = False

    @abstractmethod
    def connect(self) -> bool:
        return True
    

    @abstractmethod
    def work(self) -> None:
        if not self.get_status_work():
            for sensor in self.get_sensors():
                sensor.set_value(0)
            return False
        return True
    
    @abstractmethod
    def disconnect(self) -> bool:
        return False
    
    def get_data(self):
        data = {}
        for sensor in self.sensors:
            data[sensor.name] = f"{sensor.value}{sensor.unit}"
        return data
    
    def add_sensors(self, sensor: [Sensor, list]):
        if isinstance(sensor, list):
            self.sensors.extend(sensor)
        else:
            self.sensors.append(sensor)

    
    def set_sensor_value(self, id_sensor, value):
        for i, sensor in enumerate(self.get_sensors()):
            if i == id_sensor:
                return sensor.set_value(value)


    def get_status_work(self):
        return self.status_work
    
    def set_status_work(self, item: bool):
        self.status_work = item
        return self.status_work


    def get_status_connect(self) -> bool:
        return self.status_connect


    def get_sensors(self) -> any:
        return self.sensors
    

    def __str__(self, name) -> str:
        return f"{self.name_device} {name}"


class Bulb(Device):

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        
        self.add_sensors([Sensor("Цветовая температура", "K"), Sensor("Напряжение", "B")])


    def connect(self) -> bool:
        self.status_connect = super().connect()
        return self.status_connect
    
    def disconnect(self) -> bool:
        self.status_connect = super().disconnect()
        return self.status_connect
    
    def work(self):
        if self.get_status_work():
            self.set_sensor_value(0, 2800 + randint(-500, 1000))
            self.set_sensor_value(1, 220 + randint(-2, 3))
        
        return super().work()
            
    def __str__(self) -> str:
        return super().__str__(self.name)
    

class Socket(Device):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        
        self.add_sensors(Sensor("Напряжение", "B"))

    def work(self):
        if self.get_status_work():
            self.set_sensor_value(0, 220 + randint(-2, 3))
        return super().work()

    def connect(self) -> bool:
        self.status_connect = super().connect()
        return self.status_connect
    
    def disconnect(self) -> bool:
        self.status_connect = super().disconnect()
        return self.status_connect
    
    def __str__(self) -> str:
        return super().__str__(self.name)
    

class Kettle(Device):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

        self.add_sensors([Sensor("Вода", "Л"), Sensor("Напряжение", "B")])

    def work(self):
        if self.get_status_work():
            self.set_sensor_value(0, 20)
            self.set_sensor_value(1, 220 + randint(-2, 3))
        return super().work()
    def connect(self) -> bool:
        self.status_connect = super().connect()
        return self.status_connect
    
    def disconnect(self) -> bool:
        self.status_connect = super().disconnect()
        return self.status_connect
    
    def __str__(self) -> str:
        return super().__str__(self.name)


class Thermometer(Device):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

        self.add_sensors(Sensor("Температура", "C"))

    def work(self):
        if self.get_status_work():
            self.set_sensor_value(0, 6 + randint(-10, 5))
        return super().work()

    def connect(self) -> bool:
        self.status_connect = super().connect()
        return self.status_connect
    
    def disconnect(self) -> bool:
        self.status_connect = super().disconnect()
        return self.status_connect
    
    def __str__(self) -> str:
        return super().__str__(self.name)

    
class User:

    def __init__(self, name: str, db:Client) -> None:
        self.name = name
        self.db = db
        self.devices = []

    
    def add_device(self, device: [Device, list]):
        if isinstance(device, list):
            self.devices.extend(device)
        else:
            self.devices.append(device)

    
    def get_devices(self) -> list[Device]:
        return self.devices


    def get_device(self, id: int) -> Device:
        for i, device in enumerate(self.devices):
            if i == id:
                return device
    

    def connect_devices(self):
        for device in self.devices:
            status = device.connect()
            if status:
                self.db.log_status_connect(device, self.name)

    
    def disconnect_device(self, id: int):
        device = self.get_device(id)
        result = device.disconnect()
        self.db.log_status_connect(device, self.name)
        return result


    def connect_device(self, id: int):
        device = self.get_device(id)
        result = device.connect()
        self.db.log_status_connect(device, self.name)
        return result
    

    def off_device(self, id: int):
        device = self.get_device(id)
        result = device.set_status_work(False)
        self.db.log_status_work(device, self.name)
        return result
    
    def on_device(self, id: int):
        device = self.get_device(id)
        result = device.set_status_work(True)
        self.db.log_status_work(device, self.name)
        return result