import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Session(requests.Session):
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    timeout: float
    base_url: str
    backoff_factor: float

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        self.max_retries = max_retries

        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )
        adapter = TimeoutHTTPAdapter(timeout=self.timeout, max_retries=retry_strategy)
        self.mount("https://", adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:  # type: ignore
        query = f"{self.base_url}/{url}"
        return super().get(query, *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:  # type: ignore
        query = f"{self.base_url}/{url}"
        return super().post(query, *args, **kwargs)
