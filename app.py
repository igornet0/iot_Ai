from flask import Flask, render_template, request
from models import *
from logger import Client

app = Flask(__name__)
client_db = Client("db")

user = User("Test", client_db)

dv1 = Bulb("Кухня")
dv2 = Socket("Кухня")
dv3 = Socket("Спальня")
dv4 = Bulb("Спальня")
dv5 = Kettle("1")
dv6 = Thermometer("Улица")
dv7 = Kettle("2")

user.add_device([dv1, dv2, dv3, dv4, dv5, dv6, dv7])

@app.route('/')
def start_page():
    devices = user.get_devices()
    result = []
    for i, device in enumerate(devices):
        if device.work():
            f = str(device)
            client_db.log_data_to_mongodb(device, device.get_data())
            print(client_db.get_data(device.name_device_en))
        result.append([i, device])
    return render_template('main.html', devices=result)


@app.route('/connect')
def connect():
    id = int(request.args.get('deviceId', ''))
    return [user.connect_device(id)]

@app.route('/disconnect')
def disconnect():
    id = int(request.args.get('deviceId', ''))
    return [user.disconnect_device(id)]


@app.route('/off')
def off():
    id = int(request.args.get('deviceId', ''))
    return [user.off_device(id)]

@app.route('/on')
def on():
    id = int(request.args.get('deviceId', ''))
    return [user.on_device(id)]

if __name__ == '__main__':
    app.run(debug=True)
