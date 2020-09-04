# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## Unreleased

### Added

- Completing chapter 8
- Completed upto chapter 9.3
- Errors in yaplox are printed to stderr
- generate_ast.py now converts CamelCase fieldnames to snake_case

# Fixed

- Changed parser._match to accept an arbitrary number of tokens. A list is no
  longer required.

## [0.0.4] - 2020-09-03

### Added

- Completing chapter 8
- Added Stmt class
- Add isort to ast generator
- Create a config with classyconf
- Make imports configurable in ast generator
- Create Environment
- Variables work!

## [0.0.4] - 2020-08-23

### Added

- Completing chapter 7
- Added Interpreter, with tests
- Created YaploxRuntimeError. Yaplox calls this a RuntimeError,
but python already defines one.
- Added github actions for automated CI, automerge
- Added badges to the readme


## [0.0.3] - 2020-08-10

### Added

- Completing chapter 6
- Completed the parser

## [0.0.2] - 2020-08-06

### Added

- Completing chapter 5
- Created `tools/generate_ast.py`, added Visitor class
- Added the generated `expr.py`
- Not implemented methods in ABC base classes will raise an `NotImplementedError` that
  is ignored by coverage tests

### Fixed

- CTRL-D now works in the OSX terminal
- Refactor: Exit method is called in a single place

## [0.0.1] - 2020-08-01

### Added

- Completing chapter 4
- Created CHANGELOG.md, README.md, STATUS.md
- Created first structure of the project, including tox, flake8, mypy, black and
  other utilities
- Implemented `run`, `run_file` and `run_prompt` methods
- Added `Token`, `Scanner`, `TokenType`
- Support `strings`, `numbers` and `identifiers`

[Unreleased]: https://github.com/RoelAdriaans/yaplox/compare/v0.0.4...HEAD
[0.0.4]: https://github.com/RoelAdriaans/yaplox/releases/tag/v0.0.4
[0.0.3]: https://github.com/RoelAdriaans/yaplox/releases/tag/v0.0.3
[0.0.2]: https://github.com/RoelAdriaans/yaplox/releases/tag/v0.0.2
[0.0.1]: https://github.com/RoelAdriaans/yaplox/releases/tag/v0.0.1
