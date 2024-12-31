## [Unreleased][Unreleased]

- Any planned features or known issues can be listed here.

## [2.0.1] - 2024-12-31

### Added
- Implemented a banner function with an ASCII art logo.
- Added support to view email details, including the body of the email.
- Added support to forward emails with a simple input option.
- Added an ASCII art banner at the start.- Added `bunny()` function with ASCII art.
- Updated Files: usr-bin-sh, README.md, how_to_use.md, gmail_multi_usr_bin.py and gmail_multi.py.
- Added a new requirements.txt file and added instructions.

### Changed
- Improved login functionality so that users enter email and password correctly.
- Improved error handling for file creation during initial setup.
- Added password file directory creation with error checking.
- Simplified `run_sudo_command` function for better reusability.
- Refactored database and password file creation logic for improved reliability.
- Enhanced user prompts for password setting and confirmation.
- Refactored functions to correctly display information when editing and deleting.
- Modified password prompts to clearly distinguish between sudo and phone passwords.
- Changed default shebang to `/usr/bin/env python3` to better manage environments.
- Corrected display output for banner ASCII art.
- Implemented checks for incorrect password attempts.
- Streamlined email reading, sending, and forward processes.
- Corrected issues with email body decoding for certain character encodings.
- Improved code structure and readability.
- Made code more modular and functions easier to use.
- Changed the variable use to reflect the code such as `EMAIL_USER`, `EMAIL_PASS` so it was clearer to understand.
- Added a `.env` file for config and passwords.
- Added a config file for settings.

### Fixed
- Fixed file permission issues, using `os.getlogin()`.
- Fixed `NameError` where the colors where not being called from the correct scope.
- Fixed the `touch` command not creating files.
- Fixed file creation logic and correct use of user variables.
- Fixed logic error when editing and deleting, it will now show contacts before prompt to use delete or edit.
- Fixed incorrect sudo password prompt and cache.
- Fixed a bug where long email subjects were being truncated incorrectly.
- Resolved issues where external IP was not being called.
- Fixed incorrect use of default parameters, that was causing issues.

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


[Unreleased]: https://github.com/yourusername/gmail-multi-cli/compare/v2.0.1...HEAD
[2.0.1]: https://github.com/yourusername/gmail-multi-cli/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/yourusername/gmail-multi-cli/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/yourusername/gmail-multi-cli/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yourusername/gmail-multi-cli/releases/tag/v1.0.0