#!/bin/bash
# Simple package validation script

set -e

echo "🧪 Testing llamaline v1.0.1 Package"
echo "===================================="

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build package
echo "📦 Building package..."
python -m build

# Check package
echo "✅ Checking package with twine..."
twine check dist/*

# Test installation in a temporary location
echo "🔧 Testing installation..."
pip install dist/llamaline-1.0.1-py3-none-any.whl --force-reinstall

# Test CLI functionality
echo "🎯 Testing CLI functionality..."
llamaline --help

echo "🧪 Testing import..."
python -c "import llamaline; print('✅ Package imports successfully')"

echo "🧪 Testing basic functionality..."
python -c "
from llamaline.llamaline import Tools
import asyncio
tools = Tools()
result = asyncio.run(tools.run_python_code('print(\"Hello from llamaline v1.0.1\")'))
print('✅ Test result:', result)
assert 'Hello from llamaline v1.0.1' in result
print('✅ All tests passed!')
"

echo ""
echo "🎉 Package validation complete!"
echo "✅ Build: SUCCESS"
echo "✅ Twine check: SUCCESS" 
echo "✅ Installation: SUCCESS"
echo "✅ CLI: SUCCESS"
echo "✅ Import: SUCCESS"
echo "✅ Functionality: SUCCESS"
echo ""
echo "Ready for release! 🚀" 