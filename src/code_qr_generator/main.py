# standard library imports
import argparse

# local imports
from full_cycle_random import FullCycleRandom
from config import Config


def main() -> None:
    """
    This function is demonstration of how to use the code-qr generator.
    :return: None
    """
    parser = argparse.ArgumentParser(description="A tool for generating unique codes.")
    parser.add_argument('-c', '--count', type=int, required=True, help="Number of codes to generate.")
    args = parser.parse_args()

    configuration = Config()
    fcr = FullCycleRandom(seed=configuration.seed, min_int=configuration.min_int, max_int=configuration.max_int)
    for _ in range(args.count):
        code = next(fcr)
        configuration.seed = code
        print(f"code {code}")
    configuration.save()  # we MUST save the seed to disk so that we can resume the series on the next run


if __name__ == "__main__":
    main()