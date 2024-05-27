from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .forms import RegistrationForm, LoginForm
from .models import *
from . import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .error import *
from .Api_devices import *

main = Blueprint('main', __name__)
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.user_page'))  # Перенаправить на главную страницу для залогиненных пользователей
    return render_template('login.html')

@main.route('/user_page')
@login_required
def user_page():
    data = {}
    for device in db.session.query(Device).filter_by(user_id=current_user.id):
        if device.name == "__hide__":
            continue

        if device.status_work == 1:
            result = device.work()
            if not result[0]:
                flash(result[1], 'error')
        data[device] = db.session.query(Sensor).filter_by(device_id=device.id).all()
        
    return render_template('user_page.html', username=current_user.username, data=data)

@main.route('/get-schedule', methods=['POST'])
def get_schedule():
    device_id = request.form.get('device_id')
    user_id = current_user.id
    schedules = Schedule.query.filter_by(device_id=device_id, user_id=user_id).all()
    if not schedules:
        return jsonify([])
    
    schedule_data = [
        {'id': schedule.id, 
        'time_on': schedule.time_on, 
        'time_off': schedule.time_off} for schedule in schedules
    ]

    return jsonify(schedule_data)

@main.route('/get-links', methods=['POST'])
def get_links():
    device_id = request.form.get('device_id')
    user_id = current_user.id
    links = DevicesLinks.query.filter_by(device_id=device_id, user_id=user_id).all()
    if not links:
        return jsonify([])
    #devices_links_data = Device.query.filter_by(user_id=user_id, id=links.append).all()
    links_data = [
        {'id': link.id, 
        'time_on': schedule.time_on, 
        'time_off': schedule.time_off} for link in links
    ]

    return jsonify(schedule_data)

@main.route('/add-link', methods=['POST'])
def add_link():
    device_id = int(request.form.get('device_id'))
    device_name = "__hide__"
    device_type = request.form['device_type']

    value_on = request.form.get('value_on')
    value_off = request.form.get('value_off')
    user_id = current_user.id
    
    if device_id and value_on and value_off:
        device = Device(user_id=user_id, name=device_name, type=device_type)
        db.session.add(link)
        db.session.commit()
        link = DevicesLinks(device_id=device_id, device_link_id=device.id, value_on=value_on, value_off=value_off, user_id=user_id)
        device.initialization_sensors()
        flash('Запись добавлена', 'success')
    return jsonify(success=True)

@main.route('/edit-link', methods=['POST'])
def adit_link():
    time_start = request.form.get('time_start')
    time_end = request.form.get('time_end')
    schedule_id = int(request.form.get('schedule_id'))
    if time_start and time_end:
        schedule = db.session.query(Schedule).filter_by(id=schedule_id).first()
        if not(schedule.time_on == time_start and schedule.time_off == time_end):
            schedule.time_on = time_start
            schedule.time_off = time_end
            db.session.commit()
            flash('Запись изменена', 'success')
    return jsonify(success=True)



@main.route('/get-schedule-time', methods=['POST'])
def get_schedule_time():
    schedule_id = int(request.form.get('schedule_id'))
    schedule = db.session.query(Schedule).filter_by(id=schedule_id).first()
    if not schedule:
        return jsonify([], success=False)
    
    schedule_data = [{'id': schedule.id, 'time_on': schedule.time_on, 'time_off': schedule.time_off}]

    return jsonify(schedule_data)

@main.route('/add-schedule', methods=['POST'])
def add_schedule():
    time_start = request.form.get('time_start')
    time_end = request.form.get('time_end')
    device_id = int(request.form.get('device_id'))
    user_id = current_user.id
    if time_start and time_end:
        schedule = Schedule(time_on=time_start, time_off=time_end, device_id=device_id, user_id=user_id)
        if validatete_date_Schedule(db, schedule):
            db.session.add(schedule)
            db.session.commit()
            flash('Запись добавлена', 'success')
            return jsonify(success=True)
    return jsonify(success=False)

@main.route('/edit-schedule', methods=['POST'])
def adit_schedule():
    time_start = request.form.get('time_start')
    time_end = request.form.get('time_end')
    schedule_id = int(request.form.get('schedule_id'))
    if time_start and time_end:
        schedule = db.session.query(Schedule).filter_by(id=schedule_id).first()
        if not(schedule.time_on == time_start and schedule.time_off == time_end):
            schedule.time_on = time_start
            schedule.time_off = time_end
            db.session.commit()
            flash('Запись изменена', 'success')
    return jsonify(success=True)

@main.route('/delete-schedule', methods=['POST'])
def delete_schedule():
    schedule_id = int(request.form.get('schedule_id'))
    # Удаление из БД
    schedule = db.session.query(Schedule).filter_by(id=schedule_id).first()
    db.session.delete(schedule)
    db.session.commit()
    return jsonify(success=True)


@main.route('/connect', methods=['POST'])
def connect():
    device_id = request.form['device_id']
    device = db.session.query(Device).filter_by(id=device_id).first()
    device.connection()
    flash('Устройство подключено', 'success')
    return redirect(url_for('main.user_page'))

@main.route('/disconnect', methods=['POST'])
def disconnect():
    device_id = request.form['device_id']
    device = db.session.query(Device).filter_by(id=device_id).first()
    device.disconnection()
    flash('Устройство отключено', 'error')
    return redirect(url_for('main.user_page'))

@main.route('/on', methods=['POST'])
def on():
    device_id = request.form['device_id']
    device = db.session.query(Device).filter_by(id=device_id).first()
    result = device.on()
    if result[0]:
        flash("Устройство включено", 'success')
    else:
        flash(result[1], 'error')
    return redirect(url_for('main.user_page'))

@main.route('/off', methods=['POST'])
def off():
    device_id = request.form['device_id']
    device = db.session.query(Device).filter_by(id=device_id).first()
    result = device.off()
    if result[0]:
        flash('Устройство выключено', 'success')
    else:
        flash(result[1], 'error')
    return redirect(url_for('main.user_page'))

@main.route('/add_device', methods=['POST'])
def add_device():
   return render_template('add_device.html',device_type=devices_type)

@main.route('/delete_device', methods=['POST'])
def delete_device():
    device_id = request.form['device_id']
    device = db.session.query(Device).filter_by(id=device_id).first()
    device.delete_device()
    flash('Device has been deleted', 'success')
    return redirect(url_for('main.user_page'))

@main.route('/save_device', methods=['POST'])
def save_device():
    device_type = request.form['device_type']
    device_name = request.form['device_name']
    user_id = current_user.id
    device = Device(user_id=user_id, name=device_name, type=device_type)
    db.session.add(device)
    db.session.commit()
    device.initialization_sensors()
    flash('Device has been created', 'success')
    return redirect(url_for('main.user_page'))

@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.user_page'))
    return render_template('register.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = db.session.query(User).filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('main.user_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@main.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return render_template('login.html')
   