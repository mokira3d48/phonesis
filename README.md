<div align="center">

### PHONESIS

![](https://img.shields.io/badge/Python-3.8-blue)
![](https://img.shields.io/badge/LICENSE-MIT-%2300557f)
![](https://img.shields.io/badge/lastest-2025--06--06-green)
![](https://img.shields.io/badge/contact-dr.mokira%40gmail.com-blueviolet)


---

</div>

Multilingual tokenization algorithm using the pronunciation phonemes of words.
It adjusts its tokenization codex directly from words in the language dictionary,
rather than from large text corpora. This technique reduces compute cost
and memory usage. It also offers the ability to continually update its codex
to support other languages.

#### Table of Contents
- [Description](#description)
- [Installation](#installation)
  - [For Linux](#for-linux)
  - [For Windows](#for-windows)
- [Usage](#uage)
- [Features](#features)
- [Tests](#tests)
- [To contribute](#to-contribute)
- [Licence](#licence)
- [Contact](#contact)


## Installation

To install the project, make sure you have Python 3.8 or later version
and `pip` installed on your machine. And then run the following command lines.

### For Linux

```bash
git clone git@github.com:mokira3d48/phonesis.git phonesis;
cd phonesis;
sudo rm -r .git;
git init;  # To create a new instance of git repository
```

And then,

1. `sudo apt install cmake python3-venv` Install *Cmake* and *Virtual env*;
2. `python3 -m venv .venv` create a virtual env into directory
named `env`;
3. `source .venv/bin/activate` activate the virtual environment named `.venv`;
4. `make install` install the requirements of this package;
5. `pip install -e .` install the package in dev mode in virtual environment;
6. `make test` run the unit test scripts located at `tests` directory;
7. `make run` run script located at `src/phonesis/__main__.py`.
8. Or Run `mycmd` as a command line to run `src/phonesis/__main__.py`.

### For Windows

```bash
git clone git@github.com:mokira3d48/phonesis.git phonesis
```

```bash
cd phonesis
```

And then, delete the hidden directory named `.git` located at the root
of the directory project.

And then,

1. Install python for windows;
2. Open your command prompt;
3. Run `python -m venv .venv` to create a virtual env into directory
named `.venv`;
4 . Run `.venv\Scripts\activate` to activate the virtual environment;
5. Run `pip install -r requirements.txt` to install the requirements
of this package or project;
6. Run `pip install -e .` install the package in dev mode in virtual
environment;
7. Run `python -m phonesis` to run main script located
at `src\phonesis\__main__.py`. Or Run `mycmd` as a command line
to run `src\phonesis\__main__.py` and start the application.


---

## Usage


## Features


## Tests

To execute the unittest, make sure you have `pytest` package installed,
and then run the following command line:

```bash
make test
```
or

```shell
pytest
```

---

## To contribute

Contributions are welcome! Please follow these steps:

1. Create a new branch for your feature (`git checkout -b feature/my-feature`);
2. Commit your changes (`git commit -m 'Adding a new feature'`);
3. Push toward the branch (`git push origin feature/my-feature`);
4. Create a new *Pull Request* or *Merge Request*.

## Licence

This project is licensed under the MIT License. See the file [LICENSE](LICENSE)
for more details, contact me please.

## Contact

For your question or suggestion, contact me please:

- **Name** : Doctor Mokira
- **Email** : dr.mokira@gmail.com
- **GitHub** : [mokira3d48](https://github.com/mokira3d48)
