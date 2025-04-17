from locust import HttpUser, task, between
import os
import random

'''
class ApiTestUser(HttpUser):
    wait_time = between(1, 5)


    @task
    def get_team(self):
        self.client.get('/about')

    # GET запрос для получения данных об отчетах
    @task
    def get_generate_report(self):
        self.client.get("/get_reports?file_id=1&session_id=1")
'''


"""
class FileUploadUser(HttpUser):
    # Определите паузу между запросами
    wait_time = between(1, 2)
    # Замените на URL вашего сервера
    upload_url = "/upload_data"

    @task
    def upload_file(self):
        # Путь к реальному файлу, который вы хотите загрузить
        file_path = "my_data.csv"

        cookies = {
            'user_id': str(1)  # Добавляем user_id в cookies
        }

        # Открываем реальный файл для отправки
        with open(file_path, 'rb') as f:
            files = {
                'data_file': (os.path.basename(file_path), f, 'text/csv')  # Имя файла, содержимое и тип
            }

            # Отправляем файл с POST-запросом
            response = self.client.post(self.upload_url, files=files, cookies=cookies)

            # Проверка, что файл загружен успешно
            if response.status_code == 200:
                print("Файл успешно загружен!")
            elif response:
                print("Ошибка загрузки файла:", response.json())
"""

class ReportGenerationUser(HttpUser):
    # Определите паузу между запросами
    wait_time = between(1, 2)

    # Замените на URL вашего сервера
    generate_report_url = "/generate_report"
    @task
    def generate_report(self):
        # Данные для формы
        form_data = {
            'file_id': 3,
            'max_inventory': 480  # Пример максимального уровня запасов
        }

        # Устанавливаем cookies для сессии (имитируем авторизацию пользователя)
        cookies = {
            'user_id': str(1)  # Передаем user_id в cookies
        }

        # Отправляем POST-запрос на сервер с данными формы и cookie
        response = self.client.post(self.generate_report_url, data=form_data, cookies=cookies)

        # Проверка, что отчет был успешно создан
        if response.status_code == 200:
            print("Отчет успешно создан!")
        else:
            print("Ошибка создания отчета:", response.json())