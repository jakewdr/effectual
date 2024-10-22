# effectual

*/ɪˈfek.tʃu.əl/ meaning effective and sucessful*

## Why?

Sometimes you want a single portable python file without having to make a platform specific executable or .pyz file!

## Setup

### Python

Firstly you will need to install a version of [python](https://www.python.org/) alongside pip, this project was originally built with [python 3.11.x](https://www.python.org/downloads/release/python-31110/) but supports pretty much any python3 version pipenv does, the version the project uses can be changed from the [Pipfile](https://github.com/jakewdr/effectual/blob/main/Pipfile)!

### Taskfile

Secondly [taskfile](https://taskfile.dev) is used to run multiple commands together, check the [website](https://taskfile.dev/installation/) for the best way to install with your operating system!

### Downloading the template

This can be done by pressing the green 'use this template button' on GitHub or running:

    git clone https://github.com/jakewdr/effectual <outputDirectory>

### pipenv and installing packages

To install pipenv simply run [(you made need to add the folder to PATH in windows)](https://github.com/Atri-Labs/atrilabs-engine/discussions/586):

    pip install --user pipenv

Then navigate to your template folder and enter the following into the command line:

    task setup

This will install all development dependencies into a virtual environment allowing the following command to work

## Running the project

### Without bundling

To run the source without bundling you can use

    task dev

This will use the packages stored in the pipenv environment and lint/format the source files

### With bundling

To bundle the source files and run the output

    task dist

This will lint/format the source files and then bundle the project and any (non development) dependencies specified in the Pipfile. *Note by default I've included requests for the template project, if you don't need this remove it using the following commands*

    pipenv uninstall requests
    pipfile lock

## To be added

- Package caching
- Specific package version install
- More config granularity
- Catching more edge cases and more robust programming

## Contributions

All contributions are welcome, I'm not the best in the world at project management but if you think you can add or improve anything please send over a pull request
