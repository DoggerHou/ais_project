import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from database.models import User, DataFile, OptimizationReport

from optim import X




# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'instance/files'
REPORT_FOLDER = 'instance/reports'
ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)



# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Главная страница
def index():
    if 'id' in session:
        data_files = DataFile.query.filter_by(user_id=session['id']).all()  # Получаем все файлы для текущего пользователя
        reports = OptimizationReport.query.filter_by(user_id=session['id']).all()  # Получаем все отчеты для пользователя
        return render_template('index.html', data_files=data_files, reports=reports)
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
            session['id'] = user.id
            return index()
        else:
            flash("Неверный пароль!", "error")
            return render_template('login.html')

    return render_template('login.html')


# Страница выхода
def logout():
    session.pop('username', None)  # Удаляем данные пользователя из сессии
    flash("Вы успешно вышли из системы.", "success")  # Добавляем flash сообщение
    return index()



# Загружает файл на сервер
def upload_data():
    """
       Загружает файл на сервер.
       ---
       tags:
         - File Upload
       summary: Загрузка файла на сервер
       consumes:
         - multipart/form-data
       parameters:
         - name: data_file
           in: formData
           type: file
           required: true
           description: Файл для загрузки.
       responses:
         200:
           description: Файл успешно загружен.
           schema:
             type: object
             properties:
               success:
                 type: boolean
                 example: true
               message:
                 type: string
                 example: "Файл успешно загружен и данные сохранены!"
         400:
           description: Ошибка загрузки файла. Например, файл не выбран или формат файла неверен.
           schema:
             type: object
             properties:
               success:
                 type: boolean
                 example: false
               error:
                 type: string
                 example: "Неправильный формат файла. Пожалуйста, загрузите файл в формате CSV."
         401:
           description: Пользователь не авторизован (редирект на /login).
         415:
           description: Неверный формат файла (не поддерживаемый).
       security:
         - cookieAuth: []
       """
    if 'id' not in session:
        return login()

    if 'data_file' not in request.files:
        flash("Нет файла для загрузки", "error")
        return jsonify({"error": "Нет файла для загрузки"}), 400

    file = request.files['data_file']

    if file.filename == '':
        flash("Нет выбранного файла", "error")
        return jsonify({"error": "Нет выбранного файла"}), 400

    if file and allowed_file(file.filename):
        user_id = session['id']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Получаем текущую дату и время
        filename = f"{user_id}_{timestamp}.csv"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Сохраняем файл в папке
        file.save(file_path)

        # Сохраняем информацию о файле в базе данных
        new_file = DataFile(user_id=user_id, file_name=filename, file_path=file_path)
        db.session.add(new_file)
        db.session.commit()
        flash("Файл успешно загружен!", "success")
        return jsonify({
            "success": True,
            "message": "Файл успешно загружен и данные сохранены!",
        })
    flash("Неправильный формат файла", "error")
    return jsonify({"success": False, "error": "Неправильный формат файла. Пожалуйста, загрузите файл в формате CSV."}), 400


# Генерация отчета
def generate_report():
    """
        Создание отчета для указанного файла.
        ---
        tags:
          - Reports
        summary: Создание отчета по данным файла
        parameters:
          - name: file_id
            in: formData
            type: integer
            required: true
            description: Идентификатор файла
          - name: max_inventory
            in: formData
            type: integer
            required: true
            description: Максимальный уровень запасов.
        responses:
          200:
            description: Отчет успешно создан.
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Отчет успешно создан и сохранен!"
                report:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    created_at:
                      type: string
                      example: "2025-04-17T04:53:00"
                    max_inventory:
                      type: integer
                      example: 500
                    total_cost:
                      type: number
                      format: float
                      example: 1500.5
                    report_file_name:
                      type: string
                      example: "report_1_23_20250417_042530.csv"
          401:
            description: Пользователь не авторизован.
          404:
            description: Файл не найден.
          500:
            description: Ошибка при обработке данных.
        security:
          - cookieAuth: []
        """
    if 'id' not in session:
        return jsonify({"error": "Не авторизован"}), 401

        # Получаем данные из формы
    file_id = request.form['file_id']  # Идентификатор файла
    max_inventory = int(request.form['max_inventory'])  # Максимальный уровень запасов
    user_id = session['id']  # Получаем ID текущего пользователя из сессии

    # Получаем файл из базы данных
    file = DataFile.query.get(file_id)
    if not file:
        return jsonify({"error": "Файл не найден"}), 404

    # Путь для сохранения отчета
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Генерация уникального имени для файла
    report_file_name = f"report_{user_id}_{file_id}_{timestamp}.csv"
    report_file_path = os.path.join(REPORT_FOLDER, report_file_name)

    # Обработка
    print('Обработка началась')
    data, total_cost = X(file.file_path, max_inventory)
    print('Обработка закончилась')

    # Запись в csv
    data.to_csv(report_file_path, index=False, sep=",")

    # Сохраняем информацию о созданном отчете в базе данных
    new_report = OptimizationReport(
        user_id=user_id,
        file_id=file_id,
        max_inventory=max_inventory,
        total_cost=total_cost,  # Суммарная стоимость
        report_file_name=report_file_name,
        report_file_path=report_file_path,
    )
    db.session.add(new_report)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Отчет успешно создан и сохранен!",
        "report": {
            "id": new_report.id,
            "created_at": new_report.created_at,
            "max_inventory": new_report.max_inventory,
            "total_cost": new_report.total_cost,
            "report_file_name": new_report.report_file_name,
        }
    })


# Получение отчетов для определенного файла и пользователя
def get_reports(file_id):
    """
    Получение всех отчётов для указанного файла.
    ---
    tags:
      - Reports
    summary: Список отчётов по файлу
    parameters:
      - name: file_id
        in: path
        type: integer
        required: true
        description: ID файла, для которого запрашиваются отчёты.
    responses:
      200:
        description: Успешный запрос. Возвращает список отчётов.
        schema:
          type: object
          properties:
            reports:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  created_at:
                    type: string
                    example: "01 January 2023, 14:30"
                  max_inventory:
                    type: number
                    format: float
                    example: 150.5
                  total_cost:
                    type: number
                    format: float
                    example: 5000.0
                  report_file_path:
                    type: string
                    example: "/reports/user1_report_2023.csv"
      401:
        description: Пользователь не авторизован (редирект на /login).
      404:
        description: Файл не найден или нет доступа.
    security:
      - cookieAuth: []
    """
    if 'id' not in session:
        return redirect(url_for('login'))

    user_id = session['id']  # Извлекаем user_id из сессии

    # Извлекаем все отчеты для данного файла+пользователя
    reports = OptimizationReport.query.filter_by(user_id=user_id, file_id=file_id).all()

    # Формируем список отчетов для отправки в клиент
    reports_data = [{
        "id": report.id,
        "created_at": report.created_at.strftime('%d %B %Y, %H:%M'),
        "max_inventory": report.max_inventory,
        "total_cost": report.total_cost,
        "report_file_path": report.report_file_path,
    } for report in reports]
    # Возвращаем данные в формате JSON
    return jsonify({"reports": reports_data})


# загрузка отчета
def download_report(report_id):
    """
    Скачивание отчета по идентификатору.
    ---
    tags:
      - Reports
    summary: Скачивание отчета
    parameters:
      - name: report_id
        in: path
        type: integer
        required: true
        description: Идентификатор отчета, который нужно скачать.
    responses:
      200:
        description: Файл успешно найден и скачан.
        schema:
          type: string
          format: binary
      404:
        description: Файл отчета не найден или отчет не существует.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Файл отчета не найден!"
      401:
        description: Пользователь не авторизован.
    security:
      - cookieAuth: []
    """
    # Получаем отчет из базы данных
    report = OptimizationReport.query.get(report_id)
    if report:
        # Путь к файлу отчета
        file_path = report.report_file_path

        # Проверка, существует ли файл по данному пути
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)  # Отправляем файл на скачивание
        else:
            flash("Файл отчета не найден!", "error")
            return jsonify({"error": "Файл отчета не найден!"}), 404
    else:
        flash("Отчет не найден", "error")
        return jsonify({"error": "Файл отчета не найден!"}), 404


# удаление отчета из модального окна
def delete_report(report_id):
    # Удаление отчета по идентификатору
    """
    Удаляет отчет по идентификатору.
    ---
    tags:
      - Reports
    summary: Удаление отчета
    parameters:
      - name: report_id
        in: path
        type: integer
        required: true
        description: Идентификатор отчета, который нужно удалить.
    responses:
      200:
        description: Отчет успешно удален.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            file_id:
              type: integer
              example: 123
      404:
        description: Отчет не найден.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Отчет не найден"
      500:
        description: Ошибка при удалении отчета (например, ошибка удаления файла).
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Ошибка при удалении отчета"
    security:
      - cookieAuth: []
    """
    # Получаем отчет из базы данных
    report = OptimizationReport.query.get(report_id)

    if report:
        # Путь к файлу отчета
        file_path = report.report_file_path
        raw_file_id = report.file_id
        # Удаляем запись из базы данных
        try:
            db.session.delete(report)
            db.session.commit()

            # Проверка, существует ли файл по данному пути
            if os.path.exists(file_path):
                os.remove(file_path)  # Удаляем файл из хранилища
                return jsonify({"success": True, 'file_id': raw_file_id}), 200  # Отправляем успешный ответ

        except Exception as e:
            db.session.rollback()  # Откатываем транзакцию в случае ошибки
            flash("Ошибка при удалении отчета", "error")
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        flash("Отчет не найден", "error")
        return jsonify({"success": False, "error": "Отчет не найден"}), 404


# удаление файлов
def delete_file(file_id):
    """
    Удаляет файл и все отчеты, связанные с этим файлом.
    ---
    tags:
      - Files
    summary: Удаление файла и его отчетов
    parameters:
      - name: file_id
        in: path
        type: integer
        required: true
        description: Идентификатор файла, который нужно удалить, включая все связанные с ним отчеты.
    responses:
      200:
        description: Файл и все связанные отчеты успешно удалены.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
      404:
        description: Файл не найден.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Файл не найден"
      500:
        description: Ошибка при удалении файла или отчетов.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Ошибка в удалении файлов"
    security:
      - cookieAuth: []
    """

    # Получаем файл из базы данных
    file = DataFile.query.get(file_id)

    if file:
        # Удаляем все отчеты, связанные с этим файлом
        reports = OptimizationReport.query.filter_by(file_id=file_id).all()
        for report in reports:
            # Удаляем файл отчета из хранилища
            if os.path.exists(report.report_file_path):
                os.remove(report.report_file_path)
            db.session.delete(report)  # Удаляем отчет из базы данных

        # Удаляем файл из хранилища
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
        # Удаляем файл из базы данных
        db.session.delete(file)
        db.session.commit()
        flash("Все файлы удалены!", "success")
        return jsonify({"success": True}), 200
    else:
        flash("Ошибка в удалении файлов!", "error")
        return jsonify({"success": False, "error": "Файл не найден"}), 404
