import logging
import os

log_file = os.path.join("D:\\AI_Coordinator_Project\\logs", "test_log.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.info("This is a test log entry.")
print(f"Log file created: {log_file}")
