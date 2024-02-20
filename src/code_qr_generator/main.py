# python
import argparse
from batch import Batch
from config import Config
from full_cycle_random import FullCycleRandom


def main() -> None:
    parser = argparse.ArgumentParser(description="A tool for generating unique codes.")
    parser.add_argument('-c', '--count', type=int, required=True, help="Number of codes to generate.")
    args = parser.parse_args()
    if not isinstance(args.count, int) or args.count < 0:
        raise ValueError("--count argument must be positive integer.")

    batch: Batch or None = None
    try:
        config = Config()
        fcr = FullCycleRandom(seed=config.seed, min_int=config.min_int, max_int=config.max_int)
        batch = Batch()

        for _ in range(args.count):
            code = next(fcr, None)
            if code is None:
                print("Reached the end of the FullCycleRandom sequence.")
                break
            config.seed = code
            print(f"code {code}")

    except Exception as e:
        if isinstance(batch, Batch):
            batch.delete()
        raise

    else:
        config.save()
        print(f"Batch {batch.number} generated {args.count} codes.")


if __name__ == "__main__":
    main()