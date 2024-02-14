# standard library imports
import math
from typing import Tuple


# local imports
from src.code_qr_generator.l_f_s_r import LFSR


class FullCycleRandom:
    """
    Generate pseudo random numbers within a given range in a full cycle.
    Full cycle means that all numbers are used before repeating.

    """

    def __init__(self, min_int: int = 1, max_int: int = 100):
        """
        Initialize.

        :param min_int: The smallest random number permitted.
        :param max_int: The largest random number permitted.
        :return: Returns nothing.

        """
        if min_int <= 0:
            raise ValueError("min_int must be greater than 0")
        if min_int > max_int:
            raise ValueError("min_int must be less than max_int")
        self.min_int = min_int
        self.max_int = max_int
        bits = int(math.log2(max_int)) or 1
        self.lfsr = LFSR(bits=bits)

    def get_state(self) -> Tuple[int, int, int, int]:
        """
        Get the state, so that you can resume the series later.

        :return: A tuple of integers that define the current state of the series.
        """
        return (self.min_int, self.max_int) + self.lfsr.get_state()

    def set_state(self,  min_int: int, max_int: int, n_bits: int, register: int) -> None:
        """
        Set the state, so that you can resume a previous series or establish a known state.

        :param min_int: The smallest random number permitted.
        :param max_int: The largest random number permitted.
        :param n_bits: The number of bits in the shift register.
        :param register: Contents of the shift register, leading zeros are permitted.
        :return: Nothing.
        """
        # TODO add validation checks on the arguments
        self.min_int = min_int
        self.max_int = max_int
        self.lfsr.set_state(n_bits, register)

    def next(self) -> int:
        """
        Get the next number.

        :return: The next integer in the pseudo random series.
        """
        result = self.lfsr.next()
        while not (self.min_int <= result <= self.max_int):
            result = self.lfsr.next()
        return result
