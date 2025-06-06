# 🐍 Conda Distribution Guide for llamaline v1.0.0

This guide covers distributing llamaline through conda channels, including conda-forge.

## 📋 Prerequisites

1. **Conda Environment**:
   ```bash
   # Install miniconda/anaconda
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   
   # Install conda-build
   conda install conda-build anaconda-client -y
   ```

2. **GitHub Release**: Ensure v1.0.0 is tagged and released on GitHub

## 🔨 Building the Package

### Option 1: Automated Build Script
```bash
chmod +x build_conda.sh
./build_conda.sh
```

### Option 2: Manual Build
```bash
conda-build conda-recipe/ --output-folder ./conda-dist/
```

## 📦 Distribution Options

### 1. Personal Anaconda.org Channel

1. **Create Account**: Sign up at https://anaconda.org
2. **Login**: `anaconda login`
3. **Upload Package**:
   ```bash
   anaconda upload ./conda-dist/noarch/llamaline-1.0.0-py_0.tar.bz2
   ```
4. **Install**: Users can install with:
   ```bash
   conda install -c your-username llamaline
   ```

### 2. Conda-Forge (Recommended)

conda-forge is the community-driven conda channel with high-quality packages.

#### Step-by-Step conda-forge Submission:

1. **Fork the staged-recipes repository**:
   ```bash
   # Go to https://github.com/conda-forge/staged-recipes
   # Click "Fork" button
   git clone https://github.com/YOUR-USERNAME/staged-recipes.git
   cd staged-recipes
   ```

2. **Create recipe directory**:
   ```bash
   mkdir recipes/llamaline
   cp /path/to/llamaline/conda-recipe/meta.yaml recipes/llamaline/
   # OR use the modern format:
   cp /path/to/llamaline/conda-recipe/recipe.yaml recipes/llamaline/
   ```

3. **Update SHA256 hash**:
   ```bash
   # Get the SHA256 of the GitHub release tarball
   wget https://github.com/lukeslp/llamaline/archive/v1.0.0.tar.gz
   sha256sum v1.0.0.tar.gz
   # Update the sha256 field in the recipe
   ```

4. **Submit Pull Request**:
   ```bash
   git add recipes/llamaline/
   git commit -m "Add llamaline recipe"
   git push origin main
   # Go to GitHub and create a pull request
   ```

#### conda-forge Review Process:
- Automated checks run on your PR
- Maintainers review the recipe
- Once approved and merged, package is built automatically
- Available via: `conda install -c conda-forge llamaline`

### 3. GitHub Packages (conda)

You can also distribute via GitHub Packages:

1. **Setup GitHub registry**:
   ```bash
   conda config --add channels https://conda.pkg.github.com/lukeslp
   ```

2. **Build and upload**:
   ```bash
   conda-build conda-recipe/ --output-folder ./conda-dist/
   anaconda upload -u lukeslp ./conda-dist/noarch/llamaline-1.0.0-py_0.tar.bz2
   ```

## 🧪 Testing Installation

After building, test the package:

```bash
# Create test environment
conda create -n test-llamaline python=3.9
conda activate test-llamaline

# Install from local build
conda install -c ./conda-dist/ llamaline

# Test the installation
llamaline --help
llamaline "say hello"
```

## 📝 Recipe Files Explained

### `meta.yaml` (Traditional Format)
- Used by conda-build
- YAML format with specific sections
- Located in `conda-recipe/meta.yaml`

### `recipe.yaml` (Modern Format)
- New format preferred by conda-forge
- More flexible and powerful
- Located in `conda-recipe/recipe.yaml`

## 🔄 Version Updates

For future releases:

1. **Update version numbers** in both recipe files
2. **Update SHA256 hash** for new GitHub release
3. **Build and test** the new package
4. **Submit update** to conda-forge (if applicable)

## 🎯 Installation Methods for Users

Once distributed, users can install llamaline via:

```bash
# From conda-forge (recommended)
conda install -c conda-forge llamaline

# From your personal channel
conda install -c your-username llamaline

# From GitHub packages
conda install -c https://conda.pkg.github.com/lukeslp llamaline
```

## 📊 Package Metadata

The conda package includes:
- **Entry point**: `llamaline` command
- **Dependencies**: colorama, rich, requests
- **Python versions**: >=3.7
- **Platform**: noarch (pure Python)
- **License**: MIT
- **Maintainer**: lukeslp

## 🔗 Useful Links

- [conda-forge documentation](https://conda-forge.org/docs/)
- [conda-build documentation](https://docs.conda.io/projects/conda-build/)
- [Anaconda.org](https://anaconda.org/)
- [conda-forge staged-recipes](https://github.com/conda-forge/staged-recipes)

## ⚡ Quick Start for Conda Users

Once published to conda-forge:

```bash
# Install
conda install -c conda-forge llamaline

# Use
llamaline "show disk usage"
llamaline
```

That's it! Your package is now available to the entire conda ecosystem. 🎉 