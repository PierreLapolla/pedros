from time import sleep

from pedros.logger import get_logger
from pedros.timed import timed


@timed
def long_func():
    sleep(0.1)


def main():
    logger = get_logger()
    logger.info("Hello World!")
    long_func()


if __name__ == "__main__":
    main()
