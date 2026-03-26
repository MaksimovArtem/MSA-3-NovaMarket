import logging

from locust import HttpUser, task, between

logger = logging.getLogger(__name__)

class CircuitBreakerUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def _log_if_fallback(self, response, request_path: str) -> bool:
        if response.status_code != 503:
            return False

        try:
            payload = response.json()
        except Exception:
            return False

        if payload == {"status": "fallback", "message": "temporarily unavailable"}:
            logger.warning("Fallback triggered for %s", request_path)
            return True

        return False

    @task(1)
    def error_requests(self):
        with self.client.get("/logistics/error", catch_response=True) as response:
            self._log_if_fallback(response, "/logistics/error")

    @task(1)
    def slow_requests(self):
        with self.client.get("/logistics/slow", catch_response=True) as response:
            self._log_if_fallback(response, "/logistics/slow")

    @task(1)
    def fast_requests(self):
        with self.client.get("/logistics/fast", catch_response=True) as response:
            self._log_if_fallback(response, "/logistics/fast")

    @task(1)
    def unavailable_requests(self):
        # Проверяем случайное поведение
        with self.client.get("/logistics/unavailable", catch_response=True) as response:
            self._log_if_fallback(response, "/logistics/unavailable")
