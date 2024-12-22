import os
from typing import List

from src.localization import load_locales


class CogManager:
    def __init__(self, root_dir: str) -> None:
        self._cogs: List[str] = []
        self._root_dir = root_dir
        self._collect_cogs()

    def _collect_cogs(self) -> None:
        for entry in os.scandir(self._root_dir):
            if entry.is_dir():
                relative_path = os.path.relpath(entry.path, self._root_dir)
                init_path = os.path.join(self._root_dir, relative_path, "__init__.py")
                if os.path.exists(init_path):
                    self._cogs.append(f"{self._cogs_dir}.{relative_path}.__init__")
                    locales_path = os.path.join(self._root_dir, relative_path, "locales")
                    load_locales(locales_path)

    @property
    def _cogs_dir(self) -> str:
        return self._root_dir.replace("/", ".")
    
    @property
    def cogs(self) -> List[str]:
        return self._cogs