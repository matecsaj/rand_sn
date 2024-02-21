# python

# standard libraries
import argparse
import json
import os

# 3rd party libraries
import barcode
from barcode.writer import ImageWriter
import qrcode

# local libraries
from batch import Batch
from config import Config
from full_cycle_random import FullCycleRandom


def generate_barcode(number: int, path: str) -> None:
    """
    Generate a barcode using Code 128C format.

    Args:
        number (int): the number that should be in the barcode
        path (str): the path where the barcode should be stored

    Returns:
        None
    """
    # Choose the barcode format
    barcode_format = 'code128'

    # Ensure the number is positive and pad with a leading zero if the length is odd
    if not isinstance(number, int) or number < 0:
        raise ValueError("number argument must be a positive integer.")
    data = str(number)
    if len(data) % 2 != 0:
        data = '0' + data  # Pad with leading zero if necessary

    # Adjustments for the ImageWriter
    options = {
        'module_width': 0.2,
        'module_height': 15.0,
        'quiet_zone': 6.5,
        'text_distance': 5.0,
        'font_size': 10,
        'background': 'white',
        'foreground': 'black',
    }

    # Create the ImageWriter with options
    writer = barcode.writer.ImageWriter()

    # Apply writer options directly to the writer instance
    # Note: This step is adjusted to correctly use the writer instance with options
    writer_options = options  # This line is not needed; options are passed directly to the writer in the save method

    # Create the barcode object without passing writer_options
    code128_class = barcode.get_barcode_class(barcode_format)
    code128 = code128_class(data, writer=writer)

    # Save the barcode as an image with writer options
    output_filename = f"bar{number}"
    code128.save(os.path.join(path, output_filename), options=writer_options)


def generate_qrcode(number: int, path: str, prefix: str) -> None:
    """
    Generate a QR code.

    Args:
        number (int): the number that should be in the barcode
        prefix (str): what should be put before the number in the QR code, example, https://mydomain.com/c/.
        path (str): the path where the barcode should be stored

    Returns:
        None
    """

    # Generate QR code
    qr = qrcode.QRCode(
        # version=1,      # size 1(small) to 40(large) or omit and use fit=True for auto
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,    # the size of each box (pixel) in the QR code
        border=4,       # recommended minimum is 4
    )
    qr.add_data(f"{prefix}{number}")
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save(os.path.join(path, f"qr{number}.png"))


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