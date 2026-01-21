from locust import HttpUser, task, between

class UniversityStudentUser(HttpUser):
    wait_time = between(1, 4)
    token = None

    def on_start(self):
        response = self.client.post("/api/v1/login/access-token", data={
            "username": "student1",
            "password": "password123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def view_subjects(self):
        if not self.token:
            return
        self.client.get("/api/v1/academic/subjects", headers=self.headers, name="Get Subjects")

    @task(3)
    def view_grades(self):
        if not self.token:
            return
        self.client.get("/api/v1/academic/grades", headers=self.headers, name="Get Grades")
    
    @task(3)
    def view_schedule(self):
        if not self.token:
            return
        self.client.get("/api/v1/academic/schedule", headers=self.headers, name="Get Schedule")
            
    @task(1)
    def get_profile(self):
        if self.token:
            self.client.get("/api/v1/users/me", headers=self.headers, name="Get Profile")
