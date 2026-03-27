from locust import HttpUser, task, between

class RateLimiterUser(HttpUser):
    wait_time = between(0.01, 0.1)

    @task
    def web_requests(self):
        self.client.get("/api/", headers={"Client-Type": "web"})

    @task
    def mobile_requests(self):
        self.client.get("/api/", headers={"Client-Type": "mobile"})