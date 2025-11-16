import logging
import logging.config
from pathlib import Path
import yaml

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging(config_path):
    """Set up logging using dictConfig or yaml config."""
    if config_path:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
        return logging.getLogger("appLogger")
    else:
        print("No config path provided, using default logging configuration.")
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("appLogger")