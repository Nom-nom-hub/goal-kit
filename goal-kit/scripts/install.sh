#!/bin/bash
# Goal-Kit Installation Script

set -e

echo "🚀 Goal-Kit Installation"
echo "========================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv found"

# Install Goal-Kit as a tool
echo "📦 Installing Goal-Kit..."
uv tool install --from .

# Verify installation
echo "🔍 Verifying installation..."
if command -v goal-kit &> /dev/null; then
    echo "✅ Goal-Kit installed successfully!"
    echo ""
    echo "🎯 Getting Started:"
    echo "   goal-kit init my-first-goal"
    echo "   goal-kit --help"
else
    echo "❌ Installation failed"
    exit 1
fi

echo ""
echo "🎉 Welcome to Goal-Driven Development!"
echo "   Transform your ideas into achievements with Goal-Kit"