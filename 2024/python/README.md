# Advent of Code - 2024 - Python

Advent of Code helper using Python notebooks in a development container.

## Installation

This project is built around Visual Studio Code (vsc) and runs in a dev container. Ensure the following are installed:

- [Visual Studio Code](#visual-studio-code)
- [Docker](#docker)

Once Visual Studio Code and Docker are installed, clone the repository and open in code.

```shell
git clone https://github.com/samuel-odinware/advent-of-code.git
code advent-of-code/2024/python
```

Upon VCS opening, you should get a notification to open in a container. Click it and let the magic happen!

The final step is to add an environment variable with your session token. Follow the steps in [Advent of Code Session Token](#advent-of-code-session-token).

### Visual Studio Code

If you do not have Visual Studio Code installed, you can download it [here](https://code.visualstudio.com/download).

You will also need to install extensions for working with dev containers in VSC.

The lightweight option is to just install [ms-vscode-remote.remote-containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

The second option is to install the extension bundle [ms-vscode-remote.vscode-remote-extensionpack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) which adds a couple addition tools that are helpful when developing in a container.

### Docker

Instructions for installing Docker can be found [here](https://docs.docker.com/engine/install/).

### Advent of Code Session Token

Use the following steps to get your AoC session cookie needed for downloading puzzle data.

1. Log in to Advent of Code and access and puzzle input page (e.g. http://adventofcode.com/2024/day/1/input)
1. Right click the page and click "inspect"
1. Navigate to the "Network" tab
1. Click on any request, and go to the "Headers" tab
1. Search through the "Request Headers" for a header named cookie.
1. You should find one value that starts with `session=`, followed by a long string of hexadecimal characters. Copy the whole value, after `session=` including all the hex characters until you hit a semicolon.
1. Save this value as an environment variable on your system using the name AOC_TOKEN or create a `.env` containing `AOC_TOKEN=<TOKEN>` (see [example.env](example.env)).

## Usage

To start working on a day simply run `just create <day_number>`. This script creates a directory, downloads needed instructions and inputs, and creates notebook(s) for the provided day number. The script checks if files already exist and only downloads as needed.

### Day 1 Walkthrough

Workflow example for day 1:

1. Run `just create 1`
1. Open `day_01/challenge_01.ipynb` in the editor
1. Write code to complete the challenge
1. Successfully complete the first challenge
1. Run `just create 1`
1. Open `day_01/challenge_02.ipynb` in the editor
1. Write code to complete the challenge
1. Successfully complete the second challenge
