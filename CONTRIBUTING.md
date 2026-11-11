# Contributing

1. Fork or clone the repository and create a new branch.
2. Set up Python in a virtual environment: `python -m venv .venv`.
3. Install dependencies: `python -m pip install -r requirements-dev.txt` (using your venv Python).
4. Run `python -m pytest -q`. FFmpeg is required for rendering tests.
5. Add a test whenever you fix a bug or change a media-processing function.
6. Avoid committing any copyrighted media, API tokens, user-specific paths, or personally identifying information.
7. Submit a pull request explaining the change and the test results.

**Code style:** Use type hints, readable function names, small testable helpers, and clear error messages. Media must be original or authorized for use.
