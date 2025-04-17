from locust import HttpUser, task, between

class GetPutTestUser(HttpUser):
    wait_time = between(1, 5)

    # Установим cookie с session['id']
    def on_start(self):
        self.client.cookies["session_id"] = 1  # Установите session

    # GET запрос на страницу "about"
    @task
    def get_about(self):
        self.client.get("/about")

    # PUT запрос для обновления данных файла
    @task
    def put_generate_report(self):
        data = {
            "session_id": 1,
            "file_id": 1,  # Пример идентификатора файла
        }
        self.client.put("/get_reports", json=data)