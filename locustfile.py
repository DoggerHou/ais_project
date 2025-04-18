from locust import HttpUser, task, between
import os
import random


class GetHTMLUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_team(self):
        self.client.get('/team')

    # GET запрос для получения данных об отчетах
    @task
    def get_generate_report(self):
        self.client.get("/get_reports?file_id=1&session_id=1")



class FileUploadUser(HttpUser):
    wait_time = between(1, 5)
    upload_url = "/upload_data"

    @task
    def upload_file(self):
        # Путь к файлу
        file_path = "my_data.csv"

        # Открываем реальный файл для отправки
        with open(file_path, 'rb') as f:
            files = { 'data_file': (os.path.basename(file_path), f, 'text/csv')}

            # Отправляем файл с POST запросом
            response = self.client.post(self.upload_url, files=files, cookies={ 'user_id': str(1)})

            # Проверка, что файл загружен успешно
            if response.status_code == 200:
                print("Файл успешно загружен!")
            else:
                print("Ошибка загрузки файла:", response.json())




class ReportGenerationUser(HttpUser):
    wait_time = between(1, 1.1)
    generate_report_url = "/generate_report"

    @task
    def generate_report(self):
        # Данные для формы
        form_data = {
            'file_id': 2,
            'max_inventory': 480 
        }

        # Отправляем POST запрос
        response = self.client.post(self.generate_report_url, data=form_data, cookies={'user_id': str(2)})

        # Проверка
        if response.status_code == 200:
            print("Отчет успешно создан!", response.json())
        else:
            print("Ошибка создания отчета:", response.json())
