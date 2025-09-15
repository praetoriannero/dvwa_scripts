import logging
import random
import time

from requests import Session, Response


class DynamicSession(Session):
    def __init__(self, *args, delay_avg: float = 0.0, delay_std: float = 0.0, **kwargs):
        self._delay_avg = delay_avg
        self._delay_std = delay_std
        self._last_request_time = None
        super().__init__(*args, **kwargs)

    def _delay(self) -> float:
        if self._last_request_time is None:
            self._last_request_time = time.time()

        needed = random.gauss(self._delay_avg, self._delay_std)
        logging.debug(f"Calculated delay {needed}")
        actual = time.time() - self._last_request_time
        logging.debug(f"Actual delay {actual}")
        net_delay = max(0.0, needed - actual)
        logging.debug(f"Sleeping {net_delay}")
        time.sleep(net_delay)
        self._last_request_time = time.time()

    def get(self, *args, **kwargs) -> Response:
        self._delay()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        self._delay()
        return super().post(*args, **kwargs)
