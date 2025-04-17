from locust import HttpUser, task, between

class ApiTestUser(HttpUser):
    wait_time = between(1, 5)


    @task
    def get_team(self):
        self.client.get('/about')

    # GET запрос для получения данных об отчетах
    @task
    def get_generate_report(self):
        self.client.get("/get_reports?file_id=1&session_id=1")