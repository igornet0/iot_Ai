from .config import *
from random import randint

class Node:

    def __init__(self, name:str, value:int) -> None:
        self.name = name
        self.value = value


def get_default_value(device_type):
    sensors = sensors_device[device_type]
    default_value = []
    for name, unit in sensors.items():
        if name == "Напряжение":
            default_value.append(Node(name, 220))
        elif device_type == "Thermometer" and name == "Температура":
            default_value.append(Node(name, 22))
        elif device_type == "AirConditioner" and name == "Температура":
            default_value.append(Node(name, 15))
        elif device_type == "Kettle" and name == "Температура":
            default_value.append(Node(name, 100))
        elif device_type == "Bulb" and name == "Температура":
            default_value.append(Node(name, 30))
        elif name == "Объём":
            default_value.append(Node(name, 600))
        elif name == "Цветовая температура":
            default_value.append(Node(name, 2800))
        else:
            default_value.append(Node(name, 0))
    
    result = {}
    for i in default_value:
        result[i.name] = i.value

    return result

def validate(device_type, sensor):
    if sensor.name == "Напряжение":
        if sensor.value > 225 or sensor.value < 218:
            return False, "Неправильное напряжение!"

    if device_type == "Blob":
        if sensor.name == "Температура":
            if sensor.value > 100:
                return False, "Лампочка горячая!"

    if device_type == "Kettle":
        if sensor.name == "Температура":
            if sensor.value > 105:
                return False, "Чайник горячей!"

        if sensor.name == "Объём":
            if sensor.value < 500:
                return False, "В чайнике мало воды!"

    return True, None


def work(device_type, sensor):
    if sensor.name == "Напряжение":
        sensor.value = 220 + randint(-10, 5)

    if device_type == "Thermometer":
        if sensor.name == "Температура":
            sensor.value = 22 +randint(-5, 10)

    if device_type == "AirConditioner":
        if sensor.name == "Температура":
            sensor.value = 15 +randint(-5, 10)

    if device_type == "Kettle":
        if sensor.name == "Температура":
            sensor.value = 100 + randint(-20, 10)

        if sensor.name == "Объём":
            sensor.value = 753 + randint(-400, 500)

    if device_type == "Bulb":
        if sensor.name == "Температура":
            sensor.value = 20 + randint(0, 10)
        elif sensor.name == "Цветовая температура":
            sensor.value = 2800 + randint(-500, 1000)
        

class Bulb:
    def __init__(self) -> None:
        self.default_values = get_default_value("Bulb")

class Socket:
    def __init__(self) -> None:
        self.default_values = get_default_value("Socket")

class Kettle:
    def __init__(self) -> None:
        self.default_values = get_default_value("Kettle")

class Thermometer:
    def __init__(self) -> None:
        self.default_values = get_default_value("Thermometer")

class SensorMove:
    def __init__(self) -> None:
        self.default_values = get_default_value("SensorMove")
    
class Ventilation:
    def __init__(self) -> None:
        self.default_values = get_default_value("Ventilation")

class AirConditioner:
    def __init__(self) -> None:
        self.default_values = get_default_value("AirConditioner")

class Camera:
    def __init__(self) -> None:
        self.default_values = get_default_value("Camera")

class Lock:
    def __init__(self) -> None:
        self.default_values = get_default_value("Lock")