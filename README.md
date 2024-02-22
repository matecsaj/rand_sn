# Project Name
# code-QR-generator

## Description

This Python tool generates serial numbers accompanied by corresponding bar and QR codes, making it ideal for secure labeling and easy scanning. It allows you to assign serial numbers to batches of physical objects, enhancing inventory management and product tracking. A standout feature of this tool is its ability to randomize the order of serial numbers, effectively masking the total quantity of items produced. This is particularly useful for maintaining operational confidentiality by preventing estimates of production volumes. For a closer look at the tool's capabilities, please refer to our output [samples](samples).
- The program uses a config file to resume where the last batch ended.
- Each batch is stored in a sequentially numbered subdirectory.
- The file serial-numbers.json contains a list of all in the batch. Many tools can import .json files.
- Bar files are rectangular barcode images. These can be printed and stuck where space is limited.
- QR files are square QR code images. If you want to create a dedicated web page for each object, you can embed a URL starter in the QR code. These can be scanned with any smartphone.
- You can resize the images to match the DPI of your printer and the expected scanner resolution.

## Installation
Instructions on how to install and configure the project are still being developed. You can do the following for now:
1. Install the current stable version of [Python](https://www.python.org). 
2. At the command line or terminal prompt enter.
`pip install -r requirements.txt`

## Upgraded
Pending; waiting for the Installation section. 

## Usage
This is a guide on how to use the project.

### Configuration

Begin by deciding how serial numbers will be generated. For each config file, do this once and only once. The command-line options are as follows:
- `-s` or `--smallest`: The lowest possible serial number. The default 1. 
- `-b` or `--biggest`: The highest possible serial number. There is no default.
- `-p` or `--prefix`: A prefix added to the start of every QR code. There is no default.
- `-c` or `--config`: The name of the config file. The default is `code-QR-generator-config`.

Sample command:
`python -m main.py -s 1000 -b 9999 -p https://your-domain.com/serial-number/ -c your-config-filename'

### Batching
After setting up configuration, generate a new batch of serial numbers every time you need one. The command-line options are as follows:
- `-n` or `--number`: The number of serial numbers you need in the new batch. The default is 100.
- `-c` or `--config`: The config file's name. The default is `code-QR-generator-config.json`.

Sample command:
`python -m main.py -n 10 -c your-config-filename`

### Configuration and Batching

These two cannot be combined; configure once, then create batches.


## Backup and Restore

The config file (code-QR-generator-config.json by default) is used to determine the next serial numbers and is crucial for the proper functioning of the tool. Make sure to back it up regularly.

To recover, reinstall the program and then restore the config file back into its working directory.

## Contributing

If you find room for improvement or need to ask a question, feel free to open a new issue. We also highly appreciate pull requests that come with full unit test coverage and black formatting.

## Testing

You can find the tests in the [tests](tests) folder.

## License

This project is distributed under the [MIT License](LICENSE.txt).

## Contact

For inquiries, please contact: Peter JOHN Matecsa
matecsaj@gmail.com