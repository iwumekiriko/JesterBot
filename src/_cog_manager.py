import os
from typing import List

from src.localization import load_locales


class CogManager:
    def __init__(self, root_dir: str) -> None:
        self._cogs: List[str] = []
        self._root_dir = root_dir
        self._collect_cogs()

    def _collect_cogs(self) -> None:
        for root, _, files in os.walk(self._root_dir):
            if '__init__.py' in files:
                relative_path = os.path.relpath(root, self._root_dir)
                self._cogs.append(f"{self._cogs_dir}.{relative_path}.__init__")
                load_locales(f"{self._root_dir}/{relative_path}/locales")

    @property
    def _cogs_dir(self) -> str:
        return self._root_dir.replace("/", ".")
    
    @property
    def cogs(self) -> List[str]:
        return self._cogs