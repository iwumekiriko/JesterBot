import asyncio
import functools

from src.logger import get_logger


logger = get_logger()


def loop(minutes: int = 1):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            stop_event = asyncio.Event()
            while not stop_event.is_set():
                try:
                    await func(*args, **kwargs)
                except Exception as e:
                    logger.critical("Ошибка в бесконечном цикле!\n\nОшибка:\n```%s```", e, exc_info=True)
                try:
                    await asyncio.wait_for(stop_event.wait(), timeout=minutes * 60)
                except asyncio.TimeoutError:
                    pass
            return
        return wrapper
    return decorator