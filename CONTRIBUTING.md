# Contributing to Zektra AI Gateway

Thank you for your interest in contributing to Zektra AI Gateway! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/zektraxyz/zektra-ai-gateway.git
cd zektra-ai-gateway
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Copy environment file:
```bash
cp env.example .env
# Edit .env with your API keys and wallet info
```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **mypy** for type checking

Before committing:
```bash
black .
ruff check .
mypy zektra
```

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=zektra --cov-report=html
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests if applicable
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

## Versioning

We follow semantic versioning (SemVer):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

Current version: **0.1.0-beta**

## Questions?

Open an issue or reach out on Discord: https://discord.gg/zektra

