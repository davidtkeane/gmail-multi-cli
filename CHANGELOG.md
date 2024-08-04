# Changelog

All notable changes to the Gmail Multi-CLI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased][Unreleased]

- Any planned features or known issues can be listed here.

## [2.0.0][2.0.0] - 2024-07-29

### Added

- Multi-account support allowing management of up to three Gmail accounts.
- Colorful interface using the colorama library for improved readability.
- New menu option to return to account selection.

### Changed

- Restructured the main menu for better usability.
- Improved error handling and logging throughout the application.

### Fixed

- Resolved issues with email body decoding for certain character encodings.

## [1.1.0][1.1.0] - 2024-06-15

### Added

- Ability to forward emails directly from the CLI.
- Improved display of email content with better formatting.

### Changed

- Updated the requirements.txt file with new dependencies.

### Fixed

- Fixed a bug where long email subjects were being truncated incorrectly.

## [1.0.0][1.0.0] - 2024-05-01

### Added

- Initial release of Gmail Multi-CLI.
- Basic functionality to read, send, and manage emails from a single Gmail account.
- Command-line interface for interacting with Gmail.

[Unreleased]: https://github.com/yourusername/gmail-multi-cli/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/yourusername/gmail-multi-cli/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/yourusername/gmail-multi-cli/compare/v1.0.0...v1.1.0

[1.0.0]: https://github.com/yourusername/gmail-multi-cli/releases/tag/v1.0.0
