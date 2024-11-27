import asyncio
import functools
import threading
import time

from src.logger import get_logger


logger = get_logger()


def loop(minutes: int = 1):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            stop_event = threading.Event()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            def run_loop():
                while not stop_event.is_set():
                    try:
                        loop.run_until_complete(func(*args, **kwargs))
                    except Exception as e:
                        logger.critical("Ошибка в бесконечном цикле!\n\nОшибка:\n%s", e, exc_info=True)
                    time.sleep(minutes * 60)

            thread = threading.Thread(target=run_loop)
            thread.daemon = True
            thread.start()

            return stop_event

        return wrapper
    return decorator