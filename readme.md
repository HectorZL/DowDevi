# PROYECT Download Videos 

A project designed to manage and manipulate online course data. Tailor-made for educators and course managers looking for efficient course data handling.

## Table of Contents

- [PROYECT Download Videos](#proyect-download-videos)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setup and Installation](#setup-and-installation)
    - [Repository Cloning](#repository-cloning)
    - [Virtual Environment Configuration](#virtual-environment-configuration)
    - [Dependency Installation](#dependency-installation)
  - [Usage](#usage)
  - [Project Classes Overview](#project-classes-overview)
    - [Aux Class](#aux-class)

## Prerequisites

- **Python**: Ensure you have Python installed ([Official Download Page](https://www.python.org/downloads/)).
  
- **ffmpeg**: Ensure `ffmpeg` is installed and added to your PATH. Instructions can be found [here](https://ffmpeg.org/download.html).

- **Git**: Ensure you have Git installed ([Official Download Page](https://git-scm.com/downloads)).

- **Configure the data of edge**: Ensure you have the data of edge in the same

## Setup and Installation

### Repository Cloning

```bash
git clone [REPO_URL]
cd [REPO_DIRECTORY]
```

### Virtual Environment Configuration

Setting up a virtual environment is recommended:

```bash
python -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate  # For Windows
```

### Dependency Installation

Ensure you're using the free version of `pip`:

```bash
python -m ensurepip --default-pip
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Upon successful setup, execute the project using:

```bash
python main.py
```

## Project Classes Overview

### Aux Class

The `Aux` class provides utility functions, particularly focusing on the cleansing of file names. The key function, `clean_file_name`, takes in a file name and returns a sanitized version of it, following set criteria.


