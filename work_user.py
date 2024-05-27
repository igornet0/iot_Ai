import sqlite3

db_name = "database.db"

db = sqlite3.connect(db_name)
cursor = db.cursor()

def update_value_senser(device_id, sensor_id, value):
    cursor.execute(f"UPDATE sensors SET value={value} WHERE device_id={device_id} and id={sensor_id}")
    db.commit()

update_value_senser(1, )