from random import randint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import numpy 
import datetime
from . import db
from .Ai import log_statistics
from .Api_devices.api import Api as api_devices
from .Api_devices.config import *

def delete_data(db):
    try:
        # Перебираем все таблицы
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        print("All data deleted.")
    except Exception as e:
        db.session.rollback()
        print("Failed to delete data:", e)


def validatete_date_Schedule(db, schedule_new):
    schedules = db.session.query(Schedule).filter_by(device_id=schedule_new.device_id, time_on = schedule_new.time_on, time_off = schedule_new.time_off).all()
    return True if not schedules else False

class Log_sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(80), nullable=False)

class Log_devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(80), nullable=False)
    status_work = db.Column(db.Boolean, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_on = db.Column(db.String(80), nullable=False)
    time_off = db.Column(db.String(80), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.String(80), nullable=False, default="")
    value = db.Column(db.Integer, nullable=False, default=0)


class DevicesLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device_link_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    value_on = db.Column(db.Integer, nullable=False, default=0)
    value_off = db.Column(db.Integer, nullable=False, default=0)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    connected = db.Column(db.Integer, nullable=False, default=0)
    status_work = db.Column(db.Integer, nullable=False, default=0)

    def initialization_sensors(self):
        senosrs = [Sensor(device_id=self.id, name=name, unit=unit, value=0) for name, unit in sensors_device[self.type].items()]
        [db.session.add(sensor) for sensor in senosrs]
        db.session.commit()

    def add_link(self, device_link_id):
        link = DevicesLinks(user_id=self.user_id, device_id=self.id, device_link_id=device_link_id)
        db.session.add(link)
        db.session.commit()

    def del_link(self, device_link_id):
        link = DevicesLinks.query.filter_by(user_id=self.user_id, device_id=self.id, device_link_id=device_link_id).first()
        db.session.delete(link)
        db.session.commit()
    
    def get_links(self) -> list[DevicesLinks]:
        return db.session.query(DevicesLinks).filter_by(user_id=self.user_id, device_id=self.id)

    def get_sensors(self) -> list[Sensor]: 
        return db.session.query(Sensor).filter_by(device_id=self.id)

    def get_log_sensors(self, sensor_id) -> list[Log_sensors]:
        return db.session.query(Log_sensors).filter_by(sensor_id=sensor_id)

    def get_log_device(self) -> list[Log_devices]:
        return db.session.query(Log_devices).filter_by(device_id=self.id)

    def delete_device(self):
        for sensor in self.get_sensors():
            db.session.delete(sensor)
            for log in self.get_log_sensors(sensor.id):
                db.session.delete(log)
        for log in self.get_log_device():
            db.session.delete(log)
        for schedule in self.get_schedule():
            db.session.delete(schedule)
        for link in self.get_links():
            db.session.delete(link)
        db.session.delete(self)
        db.session.commit()

    def validatete(self, on=False) -> bool:
        sensors = self.get_sensors()
        device = api_devices(on, self.type)
        result = device.validate(sensors)
        if result[0]:
            for sensor in sensors:
                log = Log_sensors(sensor_id=sensor.id, value=sensor.value)
                db.session.add(log)
            db.session.commit()
        return result

    def on(self) -> bool:
        if self.connected and not self.status_work:
            #device = globals().get(self.type)(self.get_sensors())
            result = self.validatete(on=True)
            if result[0]:
                self.status_work = 1
                log = Log_devices(device_id=self.id, time=datetime.datetime.now(), status_work=self.status_work)
                db.session.add(log)
                db.session.commit()
            return result
        else:
            return False, "Устройство не подключено"
        
    def off(self) -> bool:
        if self.connected and self.status_work:
            self.status_work = 0
            for sensors in self.get_sensors():
                sensors.value = 0
            log = Log_devices(device_id=self.id, time=datetime.datetime.now(), status_work=self.status_work)
            db.session.add(log)
            db.session.commit()
            return True, "Устройство включено"
        else:
            return False, "Устроивоство не подключено"

    def connection(self) -> bool:
        if self.connected == 0:
            self.connected = 1
            db.session.commit()
            return True
        else:
            return False
        
    def disconnection(self) -> bool:
        if self.connected == 1:
            self.connected = 0
            self.status_work = 0
            for sensor in self.get_sensors():
                sensor.value = 0
            db.session.commit()
            return True
        else:
            return False
        
    def get_schedule(self) -> list[Schedule]:
        return db.session.query(Schedule).filter_by(device_id=self.id)
    
    def work_schedule(self) -> bool:
        time = datetime.datetime.now()
        for schedule in self.get_schedule():
            if time >= datetime.datetime.strptime(schedule.time_on, "%H:%M") and time <= datetime.datetime.strptime(schedule.time_off, "%H:%M"):
                return True
        return False

    def work_error(self):
        self.status_work = 0
        for sensor in self.get_sensors():
            sensor.value = 0

    def work(self):
        self.work_schedule()
        if self.connected and self.status_work:
            #device = globals().get(self.type)(self.get_sensors())
            result = self.validatete()
            if result[0]:
                self.status_work = 1
            else:
                self.work_error()
            db.session.commit()
            return result
        else:
            return False
        
