from sqlalchemy.orm import Session

import os
import logging
from dotenv import load_dotenv
load_dotenv()

log_level = logging.ERROR

env_value = os.getenv("ENV")
if env_value and env_value.lower() == "development":
    log_level = logging.DEBUG

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
