# type: ignore

import asyncio
import functools
import threading
import time
from typing import Callable, Awaitable

from src.logger import get_logger


logger = get_logger()


def loop1(seconds: int = 60):
    def decorator(func):
        stop_event = asyncio.Event()

        async def wrapper(self, *args, **kwargs):
            while not stop_event.is_set():
                await func(self, *args, **kwargs)
                await asyncio.sleep(seconds)

        def start(self):
            asyncio.create_task(wrapper(self))

        def stop(self):
            stop_event.set()

        wrapper.start = start
        wrapper.stop = stop

        return wrapper

    return decorator


def loop2(seconds: int = 60):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            while True:
                try:
                    await func(*args, **kwargs)
                except Exception as e:
                    logger.error("Error in looped function: %s", e, exc_info=True)
                await asyncio.sleep(seconds)
        return wrapper
    return decorator