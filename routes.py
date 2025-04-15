import os
import csv
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from database.models import User, DataFile, OptimizationReport


# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'upload_data'
ALLOWED_EXTENSIONS = {'csv'}


# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Главная страница
def index():
    return render_template('index.html')

# О проекте
def about():
    return render_template('about.html')

# О команде
def team():
    return render_template('team.html')


# Страница регистрации
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Проверка, существует ли пользователь с таким именем или email
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            # Отображаем flash сообщение, если пользователь с таким логином или email уже существует
            flash("Пользователь с таким именем или email уже существует!", "error")
            return redirect(url_for('register'))  # Перенаправляем обратно на страницу регистрации

        # Хеширование пароля с использованием pbkdf2:sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Создание нового пользователя
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Отправляем сообщение об успешной регистрации
        flash("Успешная регистрация! Введите свои данные для входа.", "success")

        return redirect(url_for('login'))  # Перенаправляем на страницу авторизации

    return render_template('register.html')


# Страница авторизации
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Поиск пользователя по имени
        user = User.query.filter_by(username=username).first()

        # Если пользователя не существует
        if user is None:
            flash("Такого пользователя не существует.", "error")
            return render_template('login.html')

        # Успешная авторизация
        if check_password_hash(user.password, password):
            session['username'] = user.username  # Сохраняем имя пользователя в сессии
            return redirect(url_for('index'))  # Перенаправляем на главную страницу
        else:
            flash("Неверный пароль!", "error")
            return render_template('login.html')

    return render_template('login.html')


# Страница выхода
def logout():
    session.pop('username', None)  # Удаляем данные пользователя из сессии
    flash("Вы успешно вышли из системы.", "success")  # Добавляем flash сообщение
    return redirect(url_for('index'))  # Перенаправляем на главную страницу



# Загрузка данных
def upload_data():
    if 'data_file' not in request.files:
        flash("Нет файла для загрузки", "error")
        return redirect(url_for('index'))

    file = request.files['data_file']

    if file.filename == '':
        flash("Нет выбранного файла", "error")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        user_id = session['user_id']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Получаем текущую дату и время
        filename = f"{user_id}_{timestamp}.csv"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Сохраняем файл в папке
        file.save(file_path)

        # Сохраняем информацию о файле в базе данных
        new_file = DataFile(user_id=user_id, file_name=filename, file_path=file_path)
        db.session.add(new_file)
        db.session.commit()

        flash("Файл успешно загружен и данные сохранены!", "success")
        return redirect(url_for('index'))  # Перенаправление на главную страницу

    flash("Неправильный формат файла. Пожалуйста, загрузите файл в формате CSV.", "error")
    return redirect(url_for('index'))


# Генерация отчета (заглушка)
def generate_report():
    if request.method == 'POST':
        # Заглушка: создание отчета с фиксированными данными
        new_report = OptimizationReport(user_id=1, file_id=1, max_inventory=480, total_cost=1500.75,
                                        report_file_name='report_2025-01-01.csv',
                                        report_file_path='/reports/report_2025-01-01.csv')
        db.session.add(new_report)
        db.session.commit()
        flash("Отчет успешно создан!", "success")
        return redirect(url_for('index'))  # Перенаправление на главную после создания отчета



# Просмотр отчетов (заглушка)
def view_report(file_id):
    # Заглушка: показываем отчеты, привязанные к файлу
    reports = OptimizationReport.query.filter_by(file_id=file_id).all()
    return render_template('index.html', reports=reports)
