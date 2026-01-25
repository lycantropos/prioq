# prioq

[![Github Actions](https://github.com/lycantropos/prioq/workflows/CI/badge.svg)](https://github.com/lycantropos/prioq/actions/workflows/ci.yml "Github Actions")
[![Codecov](https://codecov.io/gh/lycantropos/prioq/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/prioq "Codecov")
[![License](https://img.shields.io/github/license/lycantropos/prioq.svg)](https://github.com/lycantropos/prioq/blob/master/LICENSE "License")
[![PyPI](https://badge.fury.io/py/prioq.svg)](https://badge.fury.io/py/prioq "PyPI")

In what follows `python` is an alias for `python3.10` or `pypy3.10`
or any later version (`python3.11`, `pypy3.11` and so on).

## Installation

### Prerequisites

Install the latest `pip` & `setuptools` packages versions

```bash
python -m pip install --upgrade pip setuptools
```

### User

Download and install the latest stable version from `PyPI` repository

```bash
python -m pip install --upgrade prioq
```

### Developer

Download the latest version from `GitHub` repository

```bash
git clone https://github.com/lycantropos/prioq.git
cd prioq
```

Install

```bash
python -m pip install -e '.'
```

## Usage

```python
>>> from prioq.base import PriorityQueue
>>> queue = PriorityQueue(*range(10))
>>> len(queue)
10
>>> queue.peek()
0
>>> queue.pop()
0
>>> len(queue)
9
>>> queue.peek()
1
>>> queue.push(0)
>>> len(queue)
10
>>> queue.peek()
0

```

## Development

### Bumping version

#### Prerequisites

Install [bump-my-version](https://github.com/callowayproject/bump-my-version#installation).

#### Release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version

```bash
bump-my-version bump --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version

```bash
bump-my-version bump --verbose $CATEGORY
```

This will set version to `major.minor.patch`.

### Running tests

#### Plain

Install with dependencies

```bash
python -m pip install -e '.[tests]'
```

Run

```bash
pytest
```

#### `Docker` container

Run

- with `CPython`

  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```

- with `PyPy`

  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

#### `Bash` script

Run

- with `CPython`

  ```bash
  ./run-tests.sh
  ```

  or

  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`

  ```bash
  ./run-tests.sh pypy
  ```

#### `PowerShell` script

Run

- with `CPython`

  ```powershell
  .\run-tests.ps1
  ```

  or

  ```powershell
  .\run-tests.ps1 cpython
  ```

- with `PyPy`

  ```powershell
  .\run-tests.ps1 pypy
  ```
