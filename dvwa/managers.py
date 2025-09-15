from enum import Enum

import requests
from bs4 import BeautifulSoup


class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    IMPOSSIBLE = "impossible"


class CSRFManager:

    @staticmethod
    def set_csrf_token(func):
        def wrapper(*args, **kwargs):

            user_token = CSRFManager.get_token(args[0]._session, args[0].url)

            if user_token is not None:
                args[0].user_token = user_token["value"]

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_token(session: requests.Session, url: str):

        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        user_token = soup.find("input", {"name": "user_token"})
        return user_token


class DVWASessionProxy:
    login_data = {"username": "admin", "password": "password", "Login": "Login"}

    def __init__(self, url):
        super().__init__()
        self._session = requests.Session()
        self.url = f"{url}/login.php"
        self.data = {}

    @property
    def security(self):
        return self._session.cookies.get_dict()["security"]

    @security.setter
    def security(self, security_level):

        self._session.cookies.pop("security")
        self._session.cookies.set("security", security_level.value)

    @property
    def user_token(self):
        return self.data["user_token"]

    @user_token.setter
    def user_token(self, value):
        self.data["user_token"] = value

    def __enter__(self):

        self.login(
            self.url, data={**self.data, **DVWASessionProxy.login_data}
        )
        return self

    def get(self, url, headers=None, params=None):
        response = self._session.get(url, headers=headers, params=params)
        self.url = response.url
        return response

    @CSRFManager.set_csrf_token
    def login(self, url, headers=None, data=None):

        self._session.post(url, headers=headers, data={**self.data, **data})

    def post(self, url, headers=None, data=None):

        response = self._session.post(url, headers=headers, data=data)

        return response

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()


class DVWASQLiResponseParser:
    def __init__(self, response):
        self.response = response

    def get_interesting_value(self):

        soup = BeautifulSoup(self.response.content, "html.parser")
        interesting_value = soup.find("pre")
        return interesting_value

    def check_presence(self, string):
        return string in self.get_interesting_value().text
