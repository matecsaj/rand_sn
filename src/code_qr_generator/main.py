# standard library imports
import argparse
import os
import random

# local imports
from l_f_s_r import LFSR
from full_cycle_random import FullCycleRandom


# constants
seed_path_file = 'seed.txt'


def save_seed(seed: int) -> None:
    """
    :param seed: An integer representing the seed value to be saved.
    :return: None
    """
    with open(seed_path_file, 'w') as f:
        f.write(str(seed))


def load_seed() -> int:
    """
    Load seed from a file.

    :return: The loaded seed value.
    """
    with open(seed_path_file, 'r') as f:
        seed = int(f.read())
    return seed


def purge_seed() -> None:
    """
    Removes the seed file if it exists.

    :return: None
    """
    if os.path.exists(seed_path_file):
        os.remove(seed_path_file)


def main() -> None:
    """
    This function is demonstration of how to use the code-qr generator.

    :return: None
    """
    parser = argparse.ArgumentParser(description="A tool for generating unique codes.")
    parser.add_argument('-c', '--count', type=int, required=True, help="Number of codes to generate.")
    args = parser.parse_args()

    min_int = 10000
    max_int = 99999
    try:
        code = load_seed()
    except FileNotFoundError:
        code = random.randint(min_int, max_int)

    fcr = FullCycleRandom(seed=code, min_int=min_int, max_int=max_int)
    for _ in range(args.count):
        code = next(fcr)
        print(f"code {code}")
    save_seed(code)


if __name__ == "__main__":
    main()
