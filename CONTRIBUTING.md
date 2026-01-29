# Contributing to iGuide Project

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies including dev tools

```bash
pip install -r requirements.txt
```

## Code Style

This project follows PEP 8 guidelines.

### Formatting

Use `black` for code formatting:

```bash
black src/ tests/
```

### Linting

Use `flake8` for linting:

```bash
flake8 src/ tests/
```

## Testing

### Running Tests

Run all tests:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Include docstrings explaining what is being tested

## Git Workflow

1. Create a feature branch from `main`:

    ```bash
    git checkout -b feature/your-feature-name
    ```

2. Make your changes

3. Run tests and linting:

    ```bash
    pytest tests/
    black src/ tests/
    flake8 src/ tests/
    ```

4. Commit with descriptive messages:

    ```bash
    git commit -m "Add feature: description of changes"
    ```

5. Push to your fork:

    ```bash
    git push origin feature/your-feature-name
    ```

6. Create a Pull Request

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Examples:

```
Add satellite embedding extraction for municipalities
Fix database connection timeout issue
Update documentation for GEE authentication
```

## Documentation

- Update README.md for major changes
- Add docstrings to all functions and classes
- Update relevant documentation in `docs/`
- Include examples for new features

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update documentation
3. Ensure all tests pass
4. Request review from maintainers
5. Address review feedback

## Code Review Guidelines

When reviewing code:

- Check for code quality and style
- Verify tests are included and passing
- Ensure documentation is updated
- Look for potential bugs or edge cases
- Provide constructive feedback

## Questions?

If you have questions, please:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with your question

Thank you for contributing!
