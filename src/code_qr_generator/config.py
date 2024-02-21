# standard libraries
import json
import random
import os
from typing import Optional


class Config:
    seed: int
    min_int: int
    max_int: int
    _file: str = 'config.json'
    _path_file: Optional[str] = None

    def __init__(self, path: Optional[str] = None):
        """
        Initialize Config instance.

        Args:
            path (str): the path where the config file is or will be stored, defaults to the current working directory

        Returns:
            None
        """
        if path is None:
            path = os.getcwd()
        elif not os.path.isdir(path):
            raise ValueError(f"Path {path} is not a directory.")
        self._path_file = os.path.join(path, self._file)
        self.load()

    def save(self) -> None:
        """
        Save configuration to file.
        :return: None
        """
        warning = "Preserve the seed! Back-up this file and don't delete it."
        config_dict = {'*warning*': warning, 'seed': self.seed, 'min_int': self.min_int, 'max_int': self.max_int}
        with open(self._path_file, 'w') as f:
            json.dump(config_dict, f, indent=4)

    def load(self) -> None:
        """
        Load configuration from file. If not present, create.
        :return: None.
        """
        try:
            with open(self._path_file, 'r') as f:
                config_dict = json.load(f)
                self.seed = config_dict.get('seed')
                self.min_int = config_dict.get('min_int')
                self.max_int = config_dict.get('max_int')
                if not (self.min_int <= self.seed <= self.max_int):
                    raise ValueError("Range error, min_int <= seed <= max_int is required.")
        except FileNotFoundError:
            self.min_int = 100000000000
            self.max_int = 999999999999
            self.seed = random.randint(self.min_int, self.max_int)
            self.save()
