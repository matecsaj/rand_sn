# local imports
from l_f_s_r import LFSR
from full_cycle_random import FullCycleRandom


def main() -> None:
    lfsr = LFSR(bits=3)
    for _ in range(7):  # Generate 8 numbers
        print(f"next {lfsr.next()}")

    fcr = FullCycleRandom(max_int=10000)
    for _ in range(5):  # Generate 5 numbers
        print(fcr.next())

    state = fcr.get_state()
    fcr = FullCycleRandom()
    fcr.set_state(*state)
    for _ in range(5):  # Generate 5 numbers
        print(fcr.next())


if __name__ == "__main__":
    main()
