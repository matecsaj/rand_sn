# standard library imports
from functools import reduce
from typing import Dict, Tuple


class LFSR:
    """
    Fibonacci variant of a Linear Feedback Shift Registers (LFSRs).
    It is used in various applications such as pseudo-random number generation,
    digital signal processing, and in cryptographic functions.

    Reference: https://en.wikipedia.org/wiki/Linear-feedback_shift_register
    """

    optimal_taps: Dict[int, Tuple[int]] = {
        2: (2, 1),
        3: (3, 2),
        4: (4, 3),
        5: (5, 3),
        6: (6, 5),  # expected numbers 63 and got 21
        7: (7, 6),
        8: (8, 6, 5, 4),
        9: (9, 5),
        10: (10, 7),
        11: (11, 9),
        # 12: (12, 6, 4, 1),  # expected numbers 4095 and got 1365
        12: (12, 11, 10, 4),  # expected numbers 4095 and got 1365
        13: (13, 4, 3, 1),
        14: (14, 5, 3, 1),
        15: (15, 14),
        16: (16, 15, 13, 4),
        17: (17, 14),
        18: (18, 11),  # expected numbers 262143 and got 29127
        19: (19, 6, 2, 1),
        20: (20, 17),  # expected numbers 1048575 and got 209715
        21: (21, 19),  # expected numbers 2097151 and got 299593
        22: (22, 1),
        23: (23, 18),
        24: (24, 23, 22, 17),  # expected numbers 16777215 and got 5592405
        25: (25, 22),
        26: (26, 6, 2, 1),
        27: (27, 5, 2, 1),
        28: (28, 3),
        29: (29, 27),
        30: (30, 6, 4, 1),
        31: (31, 28),
        32: (31, 30, 29, 28, 26, 25, 24, 22, 21, 19, 18, 17, 14, 13, 12, 10, 8, 7, 5, 3, 2, 1),
        33: (33, 20),
        34: (34, 27),
        35: (35, 33),
        36: (36, 25),
        37: (37, 5, 4, 3, 2, 1),
        38: (38, 6, 5, 1),
        39: (39, 4),
        40: (40, 21),
        41: (41, 3),
        42: (42, 41, 20, 19),
        43: (43, 6, 4, 3),
        44: (44, 43, 18, 17),
        45: (45, 4, 3, 1),
        46: (46, 45, 26, 25),
        47: (47, 5),
        48: (48, 29),
        49: (49, 9),
        50: (50, 49, 24, 23),
        51: (51, 6, 3, 1),
        52: (52, 3),
        53: (53, 6, 2, 1),
        54: (54, 7, 6, 1),
        55: (55, 7),
        56: (56, 7, 4, 2),
        57: (57, 7, 4, 3),
        58: (58, 19),
        59: (59, 6, 5, 1),
        60: (60, 1),
        61: (61, 6, 5, 1),
        62: (62, 29, 27, 1),
        63: (63, 1),
        64: (63, 61, 60, 59),
        # Add more lengths and their optimal taps as needed,
        # optimal taps produce the longest possible sequence.
    }

    def __init__(self, seed: int = 1, bits: int = 8):
        """
        Initialize.

        :param bits: The number of bits in the shift register.
        :return: Returns nothing.

        """

        if bits not in self.optimal_taps:
            available_keys = list(self.optimal_taps.keys())
            raise ValueError(f"Invalid bits. Please choose from the following values: {available_keys}")
        self.bits = bits
        self.taps = tuple([bits - tap for tap in self.optimal_taps[bits]])  # Adjust for how Python indexes bits.
        self.register = seed & (1 << bits) - 1

    def get_state(self) -> Tuple[int, int]:
        """
        Get the state, so that you can resume the series later.

        :return: A tuple of integers that define the current state of the series.
        """

        return self.bits, self.register

    def set_state(self, bits: int, register: int) -> None:
        """
        Set the state, so that you can resume a previous series or establish a known state.

        :param bits: The number of bits in the shift register.
        :param register: Contents of the shift register, leading zeros are permitted.
        :return: Nothing.
        """

        max_register = self._max_register(bits)
        if 0 < register <= max_register:
            self.taps = self.optimal_taps[bits]
            self.bits = bits
            self.max_register = max_register
            self.register = register
        else:
            raise ValueError(f"Invalid register value. Please choose an integer between 1 and {max_register}.")

    @staticmethod
    def _max_register(n_bits: int) -> int:
        return 2 ** n_bits - 1

    def next(self) -> int:
        """
        Advance the register by one step in the series.

                1 2 3 4 5 6 7 8 (bits == 8)
               ┌─┬─┬─┬─┬─┬─┬─┬─┐
            ┌─→│0│1│0│1│0│0│1│1├─→
            │  └─┴─┴─┴┬┴┬┴─┴┬┴─┘
            └──────XOR┘ │   │
                    └──XOR──┘ (taps == 7, 5, 4)
        """
        for _ in range(self.bits):
            tap_bits = [(self.register >> tap) & 1 for tap in self.taps]
            bit = reduce(lambda x, y: x ^ y, tap_bits)
            self.register = (self.register >> 1) | (bit << (self.bits - 1))

        return self.register
