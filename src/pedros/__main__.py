from pedros.logger import setup_logging, get_logger

def main():
    setup_logging()
    logger = get_logger(__name__)
    logger.info("Hello World!")

if __name__ == "__main__":
    main()