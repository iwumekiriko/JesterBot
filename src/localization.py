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