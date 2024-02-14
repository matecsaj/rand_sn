# *** A way to run these unit tests. ***
# 1. (Open a terminal, alternately known as go to the command line.)
# 2. cd .. (Or, somehow make the project root the current directory.)
# 3. python -m unittest tests/tests

# Standard library imports
import unittest

# 3rd party libraries


# Local imports
from src.code_qr_generator.full_cycle_random import FullCycleRandom
from src.code_qr_generator.l_f_s_r import LFSR


class TestLFSR(unittest.TestCase):

    def setUp(self):
        self.lfsr = LFSR()

    def test_init(self):
        bits = 10
        lfsr = LFSR(bits=bits)
        self.assertGreater(lfsr.register, 0)
        self.assertEqual(lfsr.bits, bits)
        self.assertLess(lfsr.register, 2 ** bits)

    def test_get_state(self):
        test_bits = 4
        lfsr = LFSR(bits=test_bits)
        (bits, register) = lfsr.get_state()
        self.assertEqual(test_bits, bits)
        self.assertIsInstance(register, int)

    def test_set_state(self):
        test_n_bits = 7
        state1 = LFSR(bits=test_n_bits).get_state()
        lfsr = LFSR(bits=test_n_bits+1)
        state2 = lfsr.get_state()
        lfsr.set_state(*state1)
        state3 = lfsr.get_state()
        self.assertNotEqual(state1, state2)
        self.assertEqual(state1, state3)

    def test_next(self):
        lfsr = LFSR(40)
        first = lfsr.next()
        second = lfsr.next()
        self.assertGreater(first, 0)
        self.assertGreater(second, 0)
        self.assertNotEqual(first, second)

    def test_series_lengths(self):
        """ all possible numbers should be generated before repeating """
        for bits in LFSR.optimal_taps.keys():
            if bits > 16:   # more takes too long to run
                break

            unique_values = 2 ** bits - 1  # zero is not permitted
            generated = set()
            lfsr = LFSR(bits=bits)
            while True:
                number = lfsr.next()
                if number not in generated:
                    generated.add(number)
                else:
                    self.assertEqual(unique_values, len(generated), f"A {bits} bit series should be {unique_values} long, not {len(generated)}.")
                    break

    def test_for_missing_taps(self):
        """ The keys for the taps should start at 2 and increment. """
        last = 1
        for key in LFSR.optimal_taps.keys():
            self.assertEqual(last + 1, key)
            last = key


class TestFullCycleRandom(unittest.TestCase):

    def test_init_validation_checks(self):
        with self.assertRaises(ValueError):
            FullCycleRandom(min_int=-1, max_int=100)

        with self.assertRaises(ValueError):
            FullCycleRandom(min_int=101, max_int=100)

    # @patch("src.full_cycle_random.LFSR")
    def test_get_state(self):
        fcr = FullCycleRandom(min_int=1, max_int=10)
        expected_state = (1, 10)
        self.assertEqual(fcr.get_state()[:2], expected_state)

    def test_set_state(self):
        fcr = FullCycleRandom(min_int=3, max_int=6)
        fcr.set_state(min_int=1, max_int=10, n_bits=7, register=4)

        self.assertEqual(fcr.min_int, 1)
        self.assertEqual(fcr.max_int, 10)

    # @patch("src.full_cycle_random.LFSR.next", return_value=5)
    def test_next(self):
        fcr = FullCycleRandom(min_int=1, max_int=10)
        self.assertEqual(fcr.next(), 5)

    def test_series_length(self):
        """ All possible numbers should be generated before repeating """
        for (min_int, max_int) in ((1,7), (1, 100), (50, 100)):
            unique_values = max_int - min_int + 1
            fcr = FullCycleRandom(min_int=min_int, max_int=max_int)
            generated = set()
            while True:
                number = fcr.next()
                if number not in generated:
                    generated.add(number)
                else:
                    self.assertEqual(unique_values, len(generated))
                    break


if __name__ == "__main__":
    unittest.main()
