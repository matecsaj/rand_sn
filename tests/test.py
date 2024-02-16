# *** A way to run these unit tests. ***
# 1. (Open a terminal, alternately known as go to the command line.)
# 2. cd .. (Or, somehow make the project root the current directory.)
# 3. python -m unittest tests/tests

# Standard library imports
import unittest
import time

# 3rd party libraries


# Local imports
from src.code_qr_generator.full_cycle_random import FullCycleRandom
from src.code_qr_generator.l_f_s_r import LFSR


class TestLFSR(unittest.TestCase):

    def setUp(self):
        self.lfsr = LFSR()

    def test_init_raises(self):
        with self.assertRaises(ValueError):
            LFSR(bits=0)
        with self.assertRaises(ValueError):
            LFSR(seed=0)

    def test_init_with_seed(self):
        seed = 123
        bits = 10
        lfsr = LFSR(seed=seed, bits=bits)
        self.assertEqual(lfsr.register, seed)
        self.assertEqual(lfsr.bits, bits)
        self.assertIsInstance(lfsr.taps, tuple)
        self.assertIsInstance(lfsr, LFSR)

    def test_init_without_seed(self):
        bits = 2
        lfsr = LFSR(bits=bits)
        self.assertGreater(lfsr.register, 0)
        self.assertEqual(lfsr.bits, bits)
        self.assertIsInstance(lfsr.taps, tuple)
        self.assertIsInstance(lfsr, LFSR)

    def test_next(self):
        lfsr = LFSR()
        bits = lfsr.bits
        register = lfsr.register
        result = next(lfsr)
        self.assertEqual(lfsr.bits, bits)
        self.assertNotEqual(lfsr.register, register)
        self.assertEqual(lfsr.register, result)
        self.assertNotEqual(result, next(lfsr))

    def test_resume_series(self):
        lfsr = LFSR()
        result_a = next(lfsr)
        result_b_1 = next(lfsr)
        self.assertNotEqual(result_a, result_b_1)

        lfsr = LFSR(seed=result_a)
        result_b_2 = next(lfsr)
        self.assertEqual(result_b_1, result_b_2)

    def test_series_lengths(self):
        """ all possible numbers should be generated before repeating """
        start_time = time.time()
        timeout = 5
        for bits in LFSR.optimal_taps.keys():

            if time.time() - start_time > timeout:  # Check if 5 seconds have passed
                print(f"Breaking after {timeout} seconds for {bits} bits.")
                break  # Break out of the loop if more than 5 seconds have passed

            unique_values = 2 ** bits - 1  # zero is not permitted
            generated = set()
            lfsr = LFSR(bits=bits)
            for number in lfsr:
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

    def test_init_raises(self):
        with self.assertRaises(ValueError):
            FullCycleRandom(min_int=-1, max_int=100)
        with self.assertRaises(ValueError):
            FullCycleRandom(min_int=101, max_int=100)
        with self.assertRaises(ValueError):
            FullCycleRandom(seed=1, min_int=2, max_int=3)
        with self.assertRaises(ValueError):
            FullCycleRandom(seed=10, min_int=20, max_int=30)

    def test_init_success(self):
        min_int = 500
        max_int = 1000
        for seed in (None, 750):
            fcr = FullCycleRandom(seed=seed, min_int=min_int, max_int=max_int)
            self.assertEqual(fcr.min_int, min_int)
            self.assertEqual(fcr.max_int, max_int)
            self.assertIsInstance(fcr.lfsr, LFSR)
            self.assertIsInstance(fcr, FullCycleRandom)

    def test_next(self):
        fsr = FullCycleRandom()
        min_int = fsr.min_int
        max_int = fsr.max_int
        result = next(fsr)
        self.assertEqual(fsr.min_int, min_int)
        self.assertEqual(fsr.max_int, max_int)
        self.assertLessEqual(min_int, result)
        self.assertLessEqual(result, max_int)
        self.assertNotEqual(result, next(fsr))

    def test_resume_series(self):
        fcr = FullCycleRandom()
        result_a = next(fcr)
        result_b_1 = next(fcr)
        self.assertNotEqual(result_a, result_b_1)

        fcr = FullCycleRandom(seed=result_a)
        result_b_2 = next(fcr)
        self.assertEqual(result_b_1, result_b_2)

    def test_series_length(self):
        """ All possible numbers should be generated before repeating """
        for (min_int, max_int) in ((1, 1), (1, 7), (2, 8), (50, 100), (1, 99999)):
            unique_values = max_int - min_int + 1
            fcr = FullCycleRandom(min_int=min_int, max_int=max_int)
            generated = set()
            for number in fcr:
                if number not in generated:
                    generated.add(number)
                else:
                    self.assertEqual(unique_values, len(generated))
                    break


if __name__ == "__main__":
    unittest.main()
