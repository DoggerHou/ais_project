from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Инициализация базы данных
db = SQLAlchemy()


# Пользователь
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с файлами, загруженными пользователем
    data_files = db.relationship('DataFile', backref='user', lazy=True)

    # Связь с отчетами, сгенерированными пользователем
    optimization_reports = db.relationship('OptimizationReport', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class DataFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # путь к файлу на сервере
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с отчетами
    reports = db.relationship('OptimizationReport', backref='data_file', lazy=True)

    def __repr__(self):
        return f'<DataFile {self.file_name}>'


class OptimizationReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('data_file.id'), nullable=False)
    max_inventory = db.Column(db.Integer, nullable=False)  # максимальный уровень запасов
    total_cost = db.Column(db.Float, nullable=False)  # общая стоимость
    report_file_name = db.Column(db.String(255), nullable=False)  # имя файла отчета
    report_file_path = db.Column(db.String(255), nullable=False)  # путь к файлу отчета
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OptimizationReport {self.report_file_name}>'

