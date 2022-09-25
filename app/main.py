import logging
import random
import time
import json_log_formatter

formatter = json_log_formatter.VerboseJSONFormatter()

stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(stdout_handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    while True:
        msg = dict()
        for level in range(50):
            (
                msg[f"bid_{str(level).zfill(2)}"],
                msg[f"ask_{str(level).zfill(2)}"],
            ) = (
                random.randrange(1, 100),
                random.randrange(100, 200),
            )
        msg["stats"] = {
            "sum_bid": sum(v for k, v in msg.items() if "bid" in k),
            "sum_ask": sum(v for k, v in msg.items() if "ask" in k),
        }
        logger.info(msg)
        time.sleep(0.001)
