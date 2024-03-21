from pymongo import MongoClient
from datetime import datetime

class Client:

    def __init__(self, name_db:str) -> None:
        self.logger = []
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[name_db]


    def log_data_to_mongodb(self, device, data:str) -> bool:
        name_device = device.name_device_en
        if self.validate_data(data):
            device_data = {
                "name_device": name_device,
                "name": str(device).split()[1],
                "data": data,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.db[name_device].insert_one(device_data)
            return True
        return False

    
    def validate_data(self, data) -> bool:
        if not data == self.logger:
            self.logger = data

        return data == self.logger
    

    def get_data(self, name_device:str) -> list:
        return list(self.db[name_device].find())
