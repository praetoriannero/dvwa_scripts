import os


DVWA_DELAY_AVG = float(os.getenv("DVWA_DELAY_AVG", "0.0"))
DVWA_DELAY_STD = float(os.getenv("DVWA_DELAY_STD", "0.0"))
DVWA_URL = os.getenv("DVWA_URL", "http://127.0.0.1:8080")
DVWA_USER = os.getenv("DVWA_USER", "admin")
DVWA_PASS = os.getenv("DVWA_PASS", "password")
