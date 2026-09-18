import sys
from config.config import APP_NAME
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info(f"Starting {APP_NAME}...")
    # TODO: Initialize database, UI, and load configurations.
    logger.info("Initialization complete. Exiting for now as GUI is not yet implemented.")

if __name__ == "__main__":
    main()
