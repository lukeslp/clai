#!/bin/bash
# Release preparation script for llamaline v1.0.0

set -e

echo "🦙 llamaline v1.0.0 Release Preparation"
echo "======================================="

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if we have uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  Warning: You have uncommitted changes. Please commit them first."
    git status --short
    exit 1
fi

echo "✅ Repository is clean"

# Create and push tag
TAG="v1.0.1"
echo "🏷️  Creating tag: $TAG"

if git tag -l | grep -q "^$TAG$"; then
    echo "⚠️  Tag $TAG already exists. Deleting and recreating..."
    git tag -d $TAG
    git push origin :refs/tags/$TAG 2>/dev/null || echo "   (tag didn't exist on remote)"
fi

git tag -a $TAG -m "Release v1.0.1 - First Stable Release

🚀 Features:
- Natural language to code translation
- Interactive CLI with rich styling
- Built-in cheat sheet commands
- Safety features and confirmation prompts
- Flexible Ollama model configuration
- Full accessibility support

🛡️ Safety:
- Command confirmation before execution
- Unsafe operation blocking
- Temporary file execution for Python

📦 Distribution:
- pip installable package
- CLI entry point: llamaline
- Python 3.7+ compatibility"

echo "📤 Pushing tag to origin..."
git push origin $TAG

echo ""
echo "🎉 Release preparation complete!"
echo ""
echo "Next steps:"
echo "1. Go to GitHub: https://github.com/lukeslp/llamaline/releases"
echo "2. Click 'Draft a new release'"
echo "3. Select tag: $TAG"
echo "4. Copy the release notes from RELEASE_NOTES.md"
 