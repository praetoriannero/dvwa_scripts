import logging

from bs4 import BeautifulSoup
from requests import Session

from dvwa.globals import DVWA_USER, DVWA_PASS, DVWA_URL


def get_config() -> dict:
    data = {
        "username": DVWA_USER,
        "password": DVWA_PASS,
        "Login": "Login",
        # "user_token": get_csrf_token(session, url),
    }

    return data


def get_csrf_token(session: Session, url: str) -> str | None:
    login_page = session.get(url)
    soup = BeautifulSoup(login_page.content, "html.parser")

    csrf_token_input = soup.find("input", {"name": "user_token"})
    if csrf_token_input:
        return csrf_token_input["value"]
    else:
        return None


def login_session(
    session,
    dvwa_root_url: str = DVWA_URL,
    username: str = DVWA_USER,
    password: str = DVWA_PASS,
) -> Session | None:
    login_url = f"{dvwa_root_url}/login.php"
    data = get_config()
    data["user_token"] = get_csrf_token(session, login_url)
    response = session.post(login_url, data=data, allow_redirects=False)
    if response.status_code == 302:
        redirect_url = response.headers.get("Location")
        if redirect_url:
            if not redirect_url.startswith("http"):
                redirect_url = f"{dvwa_root_url}/{redirect_url}"

            final_response = session.get(redirect_url)

            if "Logout" in final_response.text:
                logging.debug(f"Login SUCCESSFUL - {username}:{password}")
            else:
                logging.debug(f"Login FAILED - {username}:{password}")

    return session


if __name__ == "__main__":
    from dvwa.globals import DVWA_URL

    session = Session()
    # get_session_cookie(session, DVWA_URL)
    login_session(session)
