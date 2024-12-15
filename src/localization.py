import i18n
from typing import Any


i18n.set("locale", "ru")
i18n.set("fallback", "ru")
i18n.set("enable_memoization", True)
i18n.set('file_format', 'json')
i18n.load_path.append("./src/locales")


def load_locales(path: str) -> None:
    i18n.load_path.append(path)


def get_localizator(route: str = "base"):
    def localization(key: str, **kwargs: Any) -> str:
        # TODO logs
        key = f"{route}.{key}" if route else key
        return i18n.t(key, **kwargs)
    return localization


def determine_plural_form(*args, count, **_):
    count = abs(count)
    if count % 10 >= 5 or count % 10 == 0 or (count % 100) in range(11, 20):
        return args[2]
    elif count % 10 == 1:
        return args[0]
    return args[1]

i18n.add_function("p", determine_plural_form)