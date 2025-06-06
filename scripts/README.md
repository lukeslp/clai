# 🔧 Scripts Directory

This directory contains automation scripts for llamaline development and release management.

## 📋 Scripts Overview

### `test_package.sh`
**Purpose**: Comprehensive package validation and testing

**What it does**:
- Cleans previous builds
- Builds package with `python -m build`
- Validates package with `twine check`
- Tests installation and CLI functionality
- Verifies import and basic functionality

**Usage**:
```bash
./scripts/test_package.sh
```

**Requirements**: `build`, `twine` packages installed

---

### `release.sh`
**Purpose**: GitHub release automation and tagging

**What it does**:
- Checks repository cleanliness
- Creates and pushes version tags
- Provides GitHub release instructions

**Usage**:
```bash
./scripts/release.sh
```

**Requirements**: Clean git repository, push access to origin

---

### `build_conda.sh`
**Purpose**: Conda package building and testing

**What it does**:
- Checks for conda and conda-build availability
- Builds conda package from recipe
- Provides upload instructions for anaconda.org

**Usage**:
```bash
./scripts/build_conda.sh
```

**Requirements**: `conda`, `conda-build`, `anaconda-client` installed

---

## 🚀 Typical Workflow

For a new release:

1. **Test everything**:
   ```bash
   ./scripts/test_package.sh
   ```

2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Release v1.0.x"
   git push origin main
   ```

3. **Create release**:
   ```bash
   ./scripts/release.sh
   ```

4. **Build conda package** (optional):
   ```bash
   ./scripts/build_conda.sh
   ```

## 📁 Related Files

- `conda-recipe/meta.yaml` - Traditional conda recipe
- `conda-recipe/recipe.yaml` - Modern conda-forge recipe
- `pyproject.toml` - Package configuration
- `.github/workflows/` - CI/CD automation

## 🛠 Maintenance

When updating versions:
1. Update version in `pyproject.toml`
2. Update version in `scripts/release.sh`
3. Update versions in `conda-recipe/` files
4. Run `./scripts/test_package.sh` to validate 