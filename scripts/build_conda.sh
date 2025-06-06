#!/bin/bash
# Conda package build script for llamaline v1.0.0
# Prerequisites: conda and conda-build must be installed

set -e

echo "🦙 Building llamaline v1.0.0 Conda Package"
echo "=========================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: conda is not installed or not in PATH"
    echo "Please install conda first: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Check if conda-build is available
if ! command -v conda-build &> /dev/null; then
    echo "📦 Installing conda-build..."
    conda install conda-build -y
fi

echo "✅ conda-build is available"

# Build the package
echo "🔨 Building conda package..."
conda-build conda-recipe/ --output-folder ./conda-dist/

echo ""
echo "🎉 Conda package build complete!"
echo ""
echo "📦 Package location: ./conda-dist/"
echo ""
echo "To install locally:"
echo "  conda install -c ./conda-dist/ llamaline"
echo ""
echo "To upload to anaconda.org (requires anaconda-client):"
echo "  anaconda upload ./conda-dist/noarch/llamaline-1.0.0-py_0.tar.bz2"
echo ""
echo "To upload to conda-forge:"
echo "  1. Fork https://github.com/conda-forge/staged-recipes"
echo "  2. Copy conda-recipe/ to recipes/llamaline/"
echo "  3. Submit a pull request" 