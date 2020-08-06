# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/RoelAdriaans/yaplox/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/RoelAdriaans/yaplox/releases/tag/v0.0.2
[0.0.1]: https://github.com/RoelAdriaans/yaplox/releases/tag/v0.0.1
