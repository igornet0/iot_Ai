device_RU = {"Bulb": "Лампочка", 
           "Socket": "Розетка", 
           "Kettle": "Чайник", 
           "Thermometer": "Термометр",
           "Ventilation": "Вентилятор",
           "AirConditioner": "Кондиционер",
           "Camera": "Камера",
           "Lock": "Замок",
           }

devices_type = device_RU.keys()

sensors_device = {"Bulb": {"Напряжение": "В", "Цветовая температура": "К", "Температура": "С"}, 
                 "Socket": {"Напряжение": "В"},
                 "Kettle": {"Напряжение": "В", "Температура": "С","Объём": "мл"}, 
                 "Thermometer": {"Температура": "С"},
                 "SensorMove": {"Напряжение": "В", "Движение": ""},
                 "Ventilation": {"Напряжение": "В"},
                 "AirConditioner": {"Напряжение": "В", "Температура": "С"},
                 "Camera": {"Напряжение": "В"}, 
                 "Lock": {"Напряжение": "В"},
                }


device_connect = {
    "SensorMove": "Датчик движения",
    "Thermometer": "Термометр",
}

devices_connection = device_connect.keys()