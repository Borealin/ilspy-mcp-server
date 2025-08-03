# Release Guide

This document describes how to release the package to PyPI.

## Prerequisites

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Make sure you have PyPI credentials configured:
   ```bash
   # Create ~/.pypirc or use environment variables
   # TWINE_USERNAME and TWINE_PASSWORD
   ```

## Release Process

### 1. Update Version

Update the version in `pyproject.toml`:
```toml
version = "0.1.1"  # Increment as needed
```

### 2. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/

# Build the package
python -m build
```

This creates:
- `dist/ilspy_mcp_server-X.X.X.tar.gz` (source distribution)
- `dist/ilspy_mcp_server-X.X.X-py3-none-any.whl` (wheel)

### 3. Test the Build

Test the package locally:
```bash
pip install dist/ilspy_mcp_server-*.whl
```

### 4. Check the Package

```bash
twine check dist/*
```

### 5. Upload to Test PyPI (Optional)

```bash
twine upload --repository testpypi dist/*
```

Test installation from Test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ ilspy-mcp-server
```

### 6. Upload to PyPI

```bash
twine upload dist/*
```

### 7. Verify Installation

```bash
pip install ilspy-mcp-server
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., 1.0.0)
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

## Automation (Optional)

You can automate releases using GitHub Actions. Create `.github/workflows/release.yml`:

```yaml
name: Release to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Then add your PyPI API token as a GitHub secret named `PYPI_API_TOKEN`.