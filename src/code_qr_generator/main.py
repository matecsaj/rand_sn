# python
import argparse
import json
import os

from batch import Batch
from config import Config
from full_cycle_random import FullCycleRandom


def generate_barcode(number: int, path: str) -> None:
    """
    Generate a barcode.

    Args:
        number (int): the number that should be in the barcode
        path (str): the path where the barcode should be stored

    Returns:
        None
    """
    ...     # TODO


def generate_qrcode(number: int, path: str, prefix:str) -> None:
    """
    Generate a barcode.

    Args:
        number (int): the number that should be in the barcode
        prefix (str): what should be put before the number in the QR code, example, https://mydomain.com/c/.
        path (str): the path where the barcode should be stored

    Returns:
        None
    """
    ...     # TODO


def main() -> None:
    parser = argparse.ArgumentParser(description="A tool for generating unique codes.")
    parser.add_argument('-c', '--count', type=int, required=True, help="Number of codes to generate.")
    args = parser.parse_args()
    if not isinstance(args.count, int) or args.count < 0:
        raise ValueError("--count argument must be positive integer.")

    batch: Batch or None = None
    try:
        # preparation
        config = Config()
        fcr = FullCycleRandom(seed=config.seed, min_int=config.min_int, max_int=config.max_int)
        batch = Batch()

        # get the next codes in the sequence, and the new seed
        codes: list[int] = [next(fcr) for _ in range(args.count)]
        seed = codes[-1]
        codes = sorted(codes)

        # store all codes into a file; located at the start of the batch's directory
        with open(os.path.join(batch.path_directory, 'codes.json'), 'w') as f:
            json.dump(codes, f, indent=4)

        # for each code generate a barcode image, collection located in the middle
        for code in codes:
            generate_barcode(code, batch.path_directory)

        # for each code generate a barcode image, collection located at the end
        for code in codes:
            generate_qrcode(code, batch.path_directory, prefix='https://mydomain.com/c/')

    except Exception as e:
        if isinstance(batch, Batch):
            batch.delete()
        raise

    else:
        config.seed = seed
        config.save()
        print(f"Batch {batch.number} generated {args.count} codes.")


if __name__ == "__main__":
    main()