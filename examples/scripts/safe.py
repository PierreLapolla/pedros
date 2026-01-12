import asyncio
import logging

from pedros import safe, setup_logging, get_logger

# Configure logging to see the output from @safe
setup_logging(level=logging.INFO)
logger = get_logger("safe_demo")


# 1. Basic usage: catch all exceptions and re-raise (default)
@safe
def basic_fail():
    logger.info("Executing basic_fail...")
    raise RuntimeError("Something went wrong in basic_fail")


# 2. Suppress exceptions with re_raise=False
@safe(re_raise=False)
def silent_fail():
    logger.info("Executing silent_fail (suppressed)...")
    raise ValueError("This error is logged but not raised")


# 3. Catch specific exceptions only
@safe(catch=KeyError, re_raise=False)
def specific_fail():
    logger.info("Executing specific_fail (catching KeyError)...")
    raise KeyError("Missing key!")


# 4. Using callbacks
def handle_error(e):
    logger.info(f"Custom error handler caught: {type(e).__name__}")


def cleanup():
    logger.info("Cleanup task executed in finally block")


@safe(on_error=handle_error, on_finally=cleanup, re_raise=False)
def callback_demo():
    logger.info("Executing callback_demo...")
    raise IndexError("Index out of range")


# 5. Async support
@safe(re_raise=False)
async def async_fail():
    logger.info("Executing async_fail...")
    await asyncio.sleep(0.1)
    raise ConnectionError("Lost connection")


def main():
    logger.info("--- Starting Safe Decorator Demo ---")

    # Example 1
    try:
        basic_fail()
    except RuntimeError:
        logger.info("Caught RuntimeError from basic_fail in main")

    print("-" * 30)

    # Example 2
    result = silent_fail()
    logger.info(f"silent_fail returned: {result}")

    print("-" * 30)

    # Example 3
    specific_fail()

    print("-" * 30)

    # Example 4
    callback_demo()

    print("-" * 30)

    # Example 5
    logger.info("Running async_fail...")
    asyncio.run(async_fail())

    logger.info("--- Demo Completed ---")


if __name__ == "__main__":
    main()
