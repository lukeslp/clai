#!/bin/bash
# Conda package build script for llamaline v1.0.1
# Prerequisites: conda and conda-build must be installed

set -e

echo "🦙 Building llamaline v1.0.1 Conda Package"
echo "=========================================="

# Set up conda paths
CONDA_PATHS=(
    "/home/coolhand/miniconda3/bin/conda"
    "/root/miniconda/bin/conda"
    "$(which conda 2>/dev/null || echo '')"
)

CONDA_CMD=""
for path in "${CONDA_PATHS[@]}"; do
    if [ -x "$path" ]; then
        CONDA_CMD="$path"
        break
    fi
done

if [ -z "$CONDA_CMD" ]; then
    echo "❌ Error: conda is not installed or not accessible"
    echo "Checked paths:"
    for path in "${CONDA_PATHS[@]}"; do
        echo "  - $path"
    done
    echo "Please install conda first: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Found conda at: $CONDA_CMD"

# Check if conda-build is available
CONDA_BUILD_CMD="${CONDA_CMD/\/conda/\/conda-build}"
if ! [ -x "$CONDA_BUILD_CMD" ]; then
    echo "📦 Installing conda-build..."
    "$CONDA_CMD" install conda-build -y
    # Update conda-build path after installation
    CONDA_BUILD_CMD="${CONDA_CMD/\/conda/\/conda-build}"
fi

echo "✅ conda-build is available"

# Build the package
echo "🔨 Building conda package..."
"$CONDA_BUILD_CMD" conda-recipe/ --output-folder ./conda-dist/

echo ""
echo "🎉 Conda package build complete!"
echo ""
echo "📦 Package location: ./conda-dist/"
echo ""
echo "To install locally:"
echo "  $CONDA_CMD install -c ./conda-dist/ llamaline"
echo ""
echo "To upload to anaconda.org (requires anaconda-client):"
echo "  anaconda upload ./conda-dist/noarch/llamaline-1.0.1-py_0.tar.bz2"
echo ""
echo "To upload to conda-forge:"
echo "  1. Fork https://github.com/conda-forge/staged-recipes"
echo "  2. Copy conda-recipe/ to recipes/llamaline/"
echo "  3. Submit a pull request" 