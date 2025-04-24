import os
from typing import List, Optional

from src.localization import load_locales


class CogManager:
    """
    Collects all cogs setups files in one list
    Also adds localization dirs to i18n 
    """
    def __init__(
        self,
        root_dir: str,
    ) -> None:
        self.__cogs: List[str] = []
        self.__root_dir = root_dir
        self._collect_cogs()

    def _collect_cogs(self) -> None:
        self._scan_dirs(self.__root_dir,
                        with_locales=True)

    def _scan_dirs(
        self,
        dir_path: str,
        with_locales: bool = False
    ) -> None:
        for entry in os.scandir(dir_path):
            if not entry.is_dir():
                continue

            relative_path = os.path.relpath(entry.path, dir_path)
            init_path = os.path.join(dir_path, relative_path, "__init__.py")

            if not os.path.exists(init_path):
                continue

            self.__cogs.append(f"{self._cogs_dir(dir_path)}.{relative_path}.__init__")
            if with_locales:
                locales_path = os.path.join(dir_path, relative_path, "locales")
                load_locales(locales_path)

    def _cogs_dir(self, dir_path: str) -> str:
        return dir_path.replace("/", ".")
    
    @property
    def cogs(self) -> List[str]:
        return self.__cogs
