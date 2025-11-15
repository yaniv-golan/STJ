# Contributing to the STJ Project

We welcome contributions from the community! Please read the following guidelines to help us make the contribution process smooth and effective.

## Table of Contents

- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Coding Guidelines](#coding-guidelines)
  - [Code Style](#code-style)
  - [Comments and Documentation](#comments-and-documentation)
  - [Testing](#testing)
- [Commit Messages](#commit-messages)
- [Licensing](#licensing)
- [Code of Conduct](#code-of-conduct)
- [Contact](#contact)

---

## How Can I Contribute?

### Reporting Bugs

If you find a bug or an issue, please open an issue in the [issue tracker](https://github.com/yaniv-golan/STJ/issues) and include as much detail as possible.

- **Search for existing issues** before creating a new one to avoid duplicates.
- **Provide detailed steps** to reproduce the bug.
- **Include logs or screenshots** if applicable.

### Suggesting Features

We're always looking to improve the STJ format. To suggest a new feature:

- **Open an issue** with the title starting with `Feature Request:`.
- **Provide a detailed explanation** of the feature.
- **Explain the benefits and potential drawbacks**.

### Submitting Pull Requests

We appreciate your desire to contribute code to the project. Please follow these steps:

1. **Fork the Repository**: Click the 'Fork' button in the GitHub repository and clone your fork locally.

   ```bash
   git clone https://github.com/<your-username>/STJ.git
   ```

2. **Create a New Branch**: Use a descriptive branch name.

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**: Implement your changes, following the coding guidelines.

4. **Add Tests**: Ensure that your code is covered by unit tests where applicable.

5. **Commit Changes**: Write clear and concise commit messages.

   ```bash
   git commit -am "Add feature X that does Y"
   ```

6. **Push to Your Fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**: Go to the original repository and open a pull request from your branch.

   - **Provide a clear description** of your changes.
   - **Reference related issues** if applicable.
   - **Ensure that all checks pass** before requesting a review.

---

## Coding Guidelines

### Code Style

- **Python**:
  - Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
  - Use meaningful variable and function names.
- **JavaScript**:
  - Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) or the existing code style.
- **Formatting**:
  - Consistently use either tabs or spaces (spaces are preferred).
  - Ensure code is properly indented and formatted.
- **File Naming**:
  - Use lowercase letters and underscores `_` for file names.

### Comments and Documentation

- **Comments**:
  - Write clear comments explaining non-trivial code.
  - Use docstrings for functions and classes.
- **Documentation**:
  - Update or add documentation in the `docs/` directory if applicable.
  - Ensure that any API changes are reflected in the [API Reference](api-reference.md).

### Testing

- **Unit Tests**:
  - Write unit tests for new features or bug fixes.
  - Place tests in the appropriate directory under `tests/`.
- **Test Coverage**:
  - Aim for high test coverage to ensure code reliability.
- **Running Tests**:
  - Ensure that all tests pass before submitting.

---

## Commit Messages

- **Style**:
  - Use the present tense (e.g., "Add feature" not "Added feature").
  - Be descriptive but concise.
- **Format**:
  - Start with a short summary (50 characters max).
  - Leave a blank line.
  - Provide additional details if necessary.
- **References**:
  - Reference relevant issues (e.g., `Fixes #123`).

---

## Licensing

By contributing, you agree that your contributions will be licensed under the [MIT License](./LICENSE).

---

## Code of Conduct

Please note that this project adheres to a [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## Contact

If you have any questions, feel free to reach out by opening an issue or contacting the maintainers directly.

- **Project Repository**: [STJ GitHub Repo](https://github.com/yaniv-golan/STJ)

---

Thank you for your interest in contributing!
