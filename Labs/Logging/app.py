import requests
import json
import time
from pathlib import Path
from logger import setup_logging
from functools import wraps

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

logger = setup_logging(config_path='./config.yaml')

def log_function(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Entering {func.__name__}() with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Exiting {func.__name__}() with result={result}")
                return result
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

@log_function(logger)
def fetch_api_data(url: str) -> dict:
    """Fetch JSON data from an API endpoint with retries and logging."""
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Fetching data from {url}, attempt {attempt}")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                logger.error("All retries failed.")
                raise
            time.sleep(2)

@log_function(logger)
def transform_data(raw_data: list) -> list:
    """Transform raw JSON into a structured list of records."""
    records = []
    for item in raw_data:
        records.append({
            "id": item.get("id"),
            "userId": item.get("userId"),
            "title": item.get("title", "N/A"),
            "completed": item.get("completed", False),
        })
    return records

@log_function(logger)
def validate_records(records: list) -> list:
    """Perform validation + filtering on transformed data."""
    valid = []
    for r in records:
        if r["completed"] is False:
            logger.debug(f"Dropping incomplete record: {r}")
            continue
        valid.append(r)
    return valid

@log_function(logger)
def save_to_disk(records: list, output_file: Path):
    """Save processed dataset to file with logging."""
    with open(output_file, "w") as f:
        json.dump(records, f, indent=2)
    logger.info(f"Saved {len(records)} processed records to {output_file}")

@log_function(logger)
def divide(a, b):
    return a / b


if __name__ == "__main__":
    logger.info("==== Pipeline Started ====")
    API_URL = "https://jsonplaceholder.typicode.com/todos"
    OUTPUT_FILE = DATA_DIR / "processed.json"
    try:
        raw = fetch_api_data(API_URL)
        transformed = transform_data(raw) #filter out all the incomplete tasks
        validated = validate_records(transformed)
        save_to_disk(validated, OUTPUT_FILE)
    except Exception as e:
        logger.exception(f"Pipeline failed due to: {e}")
    logger.info("==== Pipeline Finished ====")

    logger.info("App started")
    logger.debug("Debugging division logic...")
    try:
        print(divide(10, 2))
        print(divide(10, 0))
    except Exception:
        logger.error("Handled a division error")
    logger.info("App finished")