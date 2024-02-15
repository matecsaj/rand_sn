# standard library imports
import random
from typing import Optional

# local imports
from src.code_qr_generator.l_f_s_r import LFSR


class FullCycleRandom:
    """
    Generate pseudo random numbers within a given range in a full cycle.
    Full cycle means that all numbers are used before repeating.
    """

    def __init__(self, seed: Optional[int] = None, min_int: int = 1, max_int: int = 100):
        """
        Initialize FullCycleRandom instance.

        Args:
            seed (Optional[int]): Start or resume the sequence with a known integer, or None for a random start.
            min_int (int): The smallest random number permitted.
            max_int (int): The largest random number permitted.

        Returns:
            None
        """
        self.min_int = self._validate_input(value=min_int, name='min_int', min_val=1)
        self.max_int = self._validate_input(value=max_int, name='max_int', min_val=min_int)

        # determine the minimum number of bits required to store the maximum integer
        bits = max_int.bit_length()
        if bits < 2:   # edge case, LFSR requires at least two
            bits = 2

        # make or validate a seed
        if seed is None:
            seed = random.randint(self.min_int, self.max_int)
        else:
            seed = self._validate_input(value=seed, name='seed', min_val=self.min_int, max_val=self.max_int)

        # instantiate a Linear Feedback Shift Registers
        self.lfsr = LFSR(seed=seed, bits=bits)

    @staticmethod
    def _validate_input(value: int, name: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
        """
        Validate the input value.

        Args:
            value (int): The value to be validated.
            name (str): The name of the value.
            min_val (int): The minimum acceptable value.
            max_val (int): The maximum acceptable value.

        Returns:
            int: The validated value.
        """
        if not isinstance(value, int):
            raise TypeError(f'{name} must be an integer')
        if min_val is not None and value < min_val:
            raise ValueError(f".{name} can't be below {min_val}.")
        if max_val is not None and value > max_val:
            raise ValueError(f".{name} can't exceed {max_val}.")
        return value

    def __iter__(self):
        """
        Return the iterator object itself. This is required for the object
        to be used in for loops and other places where an iterable is expected.

        Returns:
            FullCycleRandom: The current class instance.
        """
        return self

    def __next__(self) -> int:
        """
        Get the next number in full cycle random sequence.

        Returns:
            int: The next number in the sequence.
        """
        for result in self.lfsr:
            if self.min_int <= result <= self.max_int:
                return result
