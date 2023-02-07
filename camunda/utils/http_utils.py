import requests

from urllib3.util.retry import Retry

from requests.adapters import HTTPAdapter

DEFAULT_TIMEOUT = 60


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs) -> None:
        self.timeout = DEFAULT_TIMEOUT

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)

retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=frozenset(["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]),
)

adapter = TimeoutHTTPAdapter(max_retries=retries)

http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
http.headers.update({"Accept": "application/json"})