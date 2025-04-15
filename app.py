from flask import Flask
from database import db
import os
from routes import index, register, login, about, team, logout, upload_data, generate_report, view_report


app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Генерируем случайный секретный ключ для приложения
db.init_app(app)

# Создание таблиц (если они ещё не существуют)
with app.app_context():
    db.create_all()


# Маршруты
app.add_url_rule('/', 'index', index)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/about', 'about', about)
app.add_url_rule('/team', 'team', team)
app.add_url_rule('/logout', 'logout', logout)  # Маршрут для выхода

# маршруты для загрузки данных и отчетов
app.add_url_rule('/upload_data', 'upload_data', upload_data, methods=['POST'])
app.add_url_rule('/generate_report', 'generate_report', generate_report, methods=['POST'])
app.add_url_rule('/view_report/<int:file_id>', 'view_report', view_report)


if __name__ == '__main__':
    app.run(debug=True)
