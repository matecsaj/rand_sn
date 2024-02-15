# local imports
from l_f_s_r import LFSR
from full_cycle_random import FullCycleRandom

# standard library imports
import os

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

    lfsr = LFSR(bits=3)
    for _ in range(7):  # Generate 8 numbers
        print(f"next {next(lfsr)}")

    # create a new full cycle random number generator with a randomly generated seed
    max_int = 10000
    fcr = FullCycleRandom(max_int=max_int)
    result = None

    # generate the first five numbers in the sequence and then save the seed
    for _ in range(5):  # Generate 5 numbers
        result = next(fcr)
        print(result)
    save_seed(result)

    # generate five more numbers by doing a for loop on the generator
    limit = 5
    for result in fcr:
        print(result)
        limit -= 1
        if limit < 0:
            break
    save_seed(result)

    # simulate resuming a full cycle number generator after shutting down and then restarting the program
    del lfsr
    fcr = FullCycleRandom(seed=load_seed(), max_int=max_int)

    # generate the next five numbers in the sequence and never continue the sequence in future
    for _ in range(5):
        print(next(fcr))
    purge_seed()


if __name__ == "__main__":
    main()
