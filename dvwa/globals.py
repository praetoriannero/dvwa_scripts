import os


_allowed_levels = ("DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR")
DVWA_LOG_LEVEL = os.getenv("DVWA_LOG_LEVEL", "INFO")
if DVWA_LOG_LEVEL not in _allowed_levels:
    raise ValueError(f"DVWA_LOG_LEVEL must be one of {_allowed_levels}")

DVWA_DELAY_AVG = float(os.getenv("DVWA_DELAY_AVG", "0.0"))
DVWA_DELAY_STD = float(os.getenv("DVWA_DELAY_STD", "0.0"))
DVWA_URL = os.getenv("DVWA_URL", "http://127.0.0.1:8080")
DVWA_USER = os.getenv("DVWA_USER", "admin")
DVWA_PASS = os.getenv("DVWA_PASS", "password")
