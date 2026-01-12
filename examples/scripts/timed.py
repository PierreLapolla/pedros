import time

from pedros import timed


@timed
def long_running_func(sleep_time: float):
    time.sleep(sleep_time)


def run_demo():
    for i in range(5):
        long_running_func(10 ** (-i))


if __name__ == "__main__":
    run_demo()
