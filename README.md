prioq
=====

[![](https://dev.azure.com/lycantropos/prioq/_apis/build/status/lycantropos.prioq?branchName=master)](https://dev.azure.com/lycantropos/prioq/_build/latest?definitionId=16&branchName=master "Azure Pipelines")
[![](https://readthedocs.org/projects/prioq/badge/?version=latest)](https://prioq.readthedocs.io/en/latest/?badge=latest "Documentation")
[![](https://codecov.io/gh/lycantropos/prioq/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/prioq "Codecov")
[![](https://img.shields.io/github/license/lycantropos/prioq.svg)](https://github.com/lycantropos/prioq/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/prioq.svg)](https://badge.fury.io/py/prioq "PyPI")

In what follows `python` is an alias for `python3.5` or `pypy3.5`
or any later version (`python3.6`, `pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions
```bash
python -m pip install --upgrade pip setuptools
```

### User

Download and install the latest stable version from `PyPI` repository:
```bash
python -m pip install --upgrade prioq
```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/prioq.git
cd prioq
```

Install dependencies
```bash
python -m pip install --force-reinstall -r requirements.txt
```

Install
```bash
python setup.py install
```

Usage
-----

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

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies
```bash
python -m pip install --force-reinstall -r requirements-tests.txt
```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
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

`PowerShell` script (e.g. can be used in `Git` hooks):
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
