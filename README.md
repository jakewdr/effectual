# effectual

*/ɪˈfek.tʃu.əl/ meaning effective and successful*

## Setup

### Python

Firstly you will need to install a version of [Python](https://www.python.org/) alongside pip, this project was originally built with [Python 3.11.x](https://www.python.org/downloads/release/python-31110/) but supports between python 3.8 and 3.13, you can refer to the uv documentation on how to change the python version of the project (make sure to change the 'task setup' command as well)


### Taskfile

Secondly [Task](https://taskfile.dev) is used to run multiple commands together, check the [website](https://taskfile.dev/installation/) for the best way to install with your operating system!

### uv

To install [uv](https://docs.astral.sh/uv/) again check the [website](https://docs.astral.sh/uv/#getting-started) for the best way for your operating system

### Downloading the template

This can be done by pressing the green 'use this template button' on GitHub or running:

    git clone https://github.com/jakewdr/effectual <outputDirectory>

### Original setup

Then navigate to your template folder and enter the following into the command line:

    task setup

This will install all development dependencies into a virtual environment allowing the following commands to work

### Installing packages correctly

When you are installing something that needs to be in the final bundle (or is imported in any of the ./src/ scripts) please use:

    uv add <packageName>

Otherwise if you are installing tooling or other things for developers just use:

    uv add --dev <packageName>

## Running the project

### In development

To run the source in development mode you can use:

    task dev

This will create a bundle in cache and update and rerun every time the source files are changed (if you keep the terminal running), note this will use the dependencies in the virtual environment and not effectual's own cache

### For production

To bundle the source files and run the output:

    task run

This will lint/format the source files, install external dependencies and then bundle the project and any (non development) dependencies specified in the pyproject.toml.

This is like what what [Rollup](https://rollupjs.org/) does for vite

## Building

To build an output bundle and not run it simply enter:

    task build