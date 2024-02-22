# standard libraries
import json
import random
import os
from typing import Optional


class Config:
    seed: int
    min_int: int
    max_int: int
    prefix: Optional[str]
    _file: str
    _path_file: Optional[str] = None
    _extension: str = '.json'

    def __init__(self,
                 path: Optional[str] = None,
                 config_filename: Optional[str] = None,
                 ):
        """
        Initialize Config instance.

        Args:
            path (str): the path where the config file is or will be stored, defaults to the current working directory
            config_filename (str): The file name without extension, example 'config'

        Returns:
            None
        """
        # path
        if path is None:
            path = os.getcwd()
        elif not os.path.isdir(path):
            raise ValueError(f"Path {path} is not a directory.")

        # filename
        if config_filename is None:
            self._file = 'code-QR-generator-config'
        else:
            self._file = config_filename
        if not self._file.endswith(self._extension):
            self._file += self._extension

        # both
        self._path_file = os.path.join(path, self._file)

    def configure(self, biggest: int, smallest: Optional[int] = 1, prefix: Optional[str] = None):
        """
        Configure when there is nothing to load from disk.

        Args:
            smallest (int): the smallest integer that that the serial number can be
            biggest (int): the biggest integer that that the serial number can be
            prefix (str): The prefix to use in QR code generation, example 'https://yourdomain.com/c/'

        Returns:
            None
        """
        self.prefix = prefix
        self.min_int = smallest
        self.max_int = biggest
        self.seed = self.min_int    # redo after validation, prevent type errors on the random call
        self._validate()
        self.seed = random.randint(self.min_int, self.max_int)

    def save(self) -> None:
        """
        Save configuration to file.
        :return: None
        """
        self._validate()
        warning = "Preserve the seed! Back-up this file and don't delete it."
        config_dict = {'*warning*': warning, 'min_int': self.min_int, 'seed': self.seed, 'max_int': self.max_int, 'prefix': self.prefix}
        with open(self._path_file, 'w') as f:
            json.dump(config_dict, f, indent=4)

    def load(self) -> None:
        """
        Load configuration from file.
        :return: None.
        """
        with open(self._path_file, 'r') as f:
            config_dict = json.load(f)
            config_dict.pop('*warning*')
            for key, value in config_dict.items():
                setattr(self, key, value)
            self._validate()

    def _validate(self) -> None:
        """
        Validate all the class variables.
        :return: None.
        """
        for (variable, value) in (('min_int', self.min_int), ('seed', self.seed), ('max_int', self.max_int)):
            if not isinstance(value, int):
                raise TypeError(f"{variable} is not an integer")
        if not (0 < self.min_int <= self.seed <= self.max_int):
            raise ValueError("Range error, 0 < min_int <= seed <= max_int is required.")

        if self.prefix is not None and not isinstance(self.prefix, str):
            raise TypeError("Prefix must be None or a string.")

        if not isinstance(self._file, str):
            raise TypeError("_file must be a string.")
        if not self._file.endswith(self._extension):
            raise ValueError(f"_file must end with {self._extension}.")
        if self._file == self._extension:
            raise ValueError(f"_file must have something before {self._extension}.")

        if not isinstance(self._path_file, str):
            raise TypeError("_path_file must be a string.")
        if not self._path_file.endswith(self._extension):
            raise ValueError(f"_path_file must end with {self._extension}.")
        if len(self._path_file) <= len(self._file):
            raise ValueError(f"the path is missing from _path_file {self._path_file}.")
