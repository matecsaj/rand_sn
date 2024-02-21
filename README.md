# Project Name
# code-QR-generator
## Description
A Python tool for generating unique, non-sequential alphanumeric codes and their corresponding QR codes, ideal for secure labeling and easy scanning.
## Table of Contents
List of sections you included in your README file.
## Installation
Instructions on how to install and configure the project are pending.
## Usage
Guide on how to use the project.
Run the program with the command line option -c 10 to generate 10 codes. Prefix QR codes with what is after 'p'.

`python -m main.py -c 10 -p https://yourdomain.com/c/`

After the first run, should the range of codes not be to your liking, then modify config.json such that the seed is a number between min and max int.
## Backup and Restore
When the program first runs it will create a config.json file in the current directory, and it will update this file upon subsequent runs. The file must be
preserved; don't delete it; ensure that it is backed up. Should you need to revert to a backup, restore the
file before running the program.
The seed stored in config.json is crucial, the program uses it to determine the next code.
## Contributing
Please make a new issue if you see an opportunity for improvement or have a question. A corresponding pull request with full unit test coverage and black formatting are welcome.
## Tests
Test are found in the test folder, the file has instructions at the top of the file.
## License
[MIT License](LICENSE.txt)