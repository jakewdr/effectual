# effectual

*/ɪˈfek.tʃu.əl/ meaning effective and sucessful*

## Why?

Sometimes you want a single portable python file without having to make a platform specific executable or .pyz file! Basically me trying to make [vite](https://vite.dev/) for python (badly)

## When not to use this

- The python package requires access to specific files like [customtkinter](https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging#windows-pyinstaller-auto-py-to-exe) and [pillow](https://python-pillow.org/)
- Incredibly version specific code, for example something that won't run on a slightly different version, this is because the user will need to have the exact same python version

## Setup

### Python

Firstly you will need to install a version of [python](https://www.python.org/) alongside pip, this project was originally built with [python 3.11.x](https://www.python.org/downloads/release/python-31110/) but supports pretty much any python3 version pipenv does, the version the project uses can be changed from the [Pipfile](https://bilard.medium.com/change-python-version-in-pipenv-1ac7b8f9b7b9), make sure to change the ruff settings to the output version as well!

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

## Keeping your projects up to date

To make sure there are no disparities between your distribution and developer packages run the following command in a separate terminal to automatically add any packages to cache:

    task background

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

- More config granularity

## Contributions

All contributions are welcome, I'm not the best in the world at project management but if you think you can add or improve anything please send over a pull request
