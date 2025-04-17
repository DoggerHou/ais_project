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



class FileUploadUser(HttpUser):
    # Определите паузу между запросами
    wait_time = between(1, 2)
    # Замените на URL вашего сервера
    upload_url = "/upload_data"

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None

    def on_start(self):
        self.user_id = 1

    @task
    def upload_file(self):
        # Путь к реальному файлу, который вы хотите загрузить
        file_path = "my_data.csv"

        cookies = {
            'user_id': str(self.user_id)  # Добавляем user_id в cookies
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
            else:
                print("Ошибка загрузки файла:", response.json())