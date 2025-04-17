from flask import Flask
from database import db
import os
from routes import index, register, login, about, team, logout, upload_data, generate_report, get_reports, download_report, delete_report, delete_file
from flasgger import Swagger
from flask_session import Session
import redis

app = Flask(__name__)
swagger = Swagger(app)

# Конфигурация базы данных
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://maloznaal:Armagedon22@localhost:3306/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Генерируем случайный секретный ключ для приложения
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # Для дополнительной безопасности
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload_data')  # Путь к папке с отчетами
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Ограничение на размер загружаемого файла

db.init_app(app)
Session(app)

# Создание таблиц (если они ещё не существуют)
with app.app_context():
    db.create_all()


# Маршруты
app.add_url_rule('/', 'index', index)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/about', 'about', about)
app.add_url_rule('/team', 'team', team)
app.add_url_rule('/logout', 'logout', logout)

# маршруты для загрузки данных и отчетов
app.add_url_rule('/upload_data', 'upload_data', upload_data, methods=['POST'])
app.add_url_rule('/generate_report', 'generate_report', generate_report, methods=['POST'])
app.add_url_rule('/get_reports', 'get_reports', get_reports, methods=['GET'])
app.add_url_rule('/download_report/<int:report_id>', 'download_report', download_report, methods=['POST'])
app.add_url_rule('/delete_report/<int:report_id>', 'delete_report', delete_report, methods=['DELETE'])
app.add_url_rule('/delete_file/<int:file_id>', 'delete_file', delete_file, methods=['DELETE'])


if __name__ == '__main__':
    app.run(debug=True)
