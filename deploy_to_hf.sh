#!/bin/bash

# 🤗 Hugging Face Spaces Deployment Script
# This script automates the deployment process

set -e  # Exit on error

echo "🚀 Hugging Face Spaces Deployment Script"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed. Please install Git first."
    exit 1
fi

# Check if git lfs is installed
if ! command -v git-lfs &> /dev/null; then
    echo "⚠️  Warning: Git LFS is not installed."
    echo "Install it with: brew install git-lfs (macOS) or apt-get install git-lfs (Linux)"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Git LFS is installed"
    git lfs install
fi

# Get Hugging Face username and space name
echo ""
echo "📝 Enter your Hugging Face details:"
read -p "Hugging Face Username: " HF_USERNAME
read -p "Space Name (e.g., nbfc-credit-scoring): " SPACE_NAME

if [ -z "$HF_USERNAME" ] || [ -z "$SPACE_NAME" ]; then
    echo "❌ Error: Username and Space Name are required"
    exit 1
fi

HF_SPACE_URL="https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"

echo ""
echo "🎯 Target Space: ${HF_SPACE_URL}"
echo ""
read -p "Have you created this Space on Hugging Face? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please create the Space first:"
    echo "1. Go to https://huggingface.co/spaces"
    echo "2. Click 'Create new Space'"
    echo "3. Select 'Docker' as SDK"
    echo "4. Then run this script again"
    exit 1
fi

# Prepare files
echo ""
echo "📦 Preparing deployment files..."

# Copy HF-specific README
cp README_HF.md README.md
echo "✅ Updated README.md"

# Use HF-specific requirements
cp requirements-hf.txt requirements.txt
echo "✅ Updated requirements.txt"

# Update README with actual URLs
sed -i.bak "s/YOUR_USERNAME/${HF_USERNAME}/g" README.md
sed -i.bak "s/YOUR_SPACE_NAME/${SPACE_NAME}/g" README.md
sed -i.bak "s|YOUR_SPACE_URL|${HF_USERNAME}-${SPACE_NAME}.hf.space|g" README.md
rm README.md.bak
echo "✅ Customized README with your Space details"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo ""
    echo "📂 Initializing Git repository..."
    git init
    git checkout -b main
fi

# Set up Git LFS for large files
echo ""
echo "📊 Setting up Git LFS for model files..."
if command -v git-lfs &> /dev/null; then
    git lfs track "*.pkl"
    git lfs track "*.bin"
    git lfs track "*.pt"
    git lfs track "*.pth"
    git add .gitattributes
fi

# Add all necessary files
echo ""
echo "➕ Adding files to git..."
git add app.py
git add enhanced_main.py
git add enhanced_scoring.py
git add scoring.py
git add bank_statement_processor.py
git add Dockerfile
git add .dockerignore
git add requirements.txt
git add README.md
git add xgb_model.pkl
git add label_encoder.pkl

# Commit
echo ""
echo "💾 Committing changes..."
git commit -m "Deploy to Hugging Face Spaces" || echo "No changes to commit"

# Add Hugging Face remote
echo ""
echo "🔗 Connecting to Hugging Face..."
git remote remove space 2>/dev/null || true
git remote add space "https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"

# Push to Hugging Face
echo ""
echo "🚀 Pushing to Hugging Face Spaces..."
echo ""
echo "⚠️  You will be prompted for credentials:"
echo "   Username: ${HF_USERNAME}"
echo "   Password: Use your Hugging Face Access Token (not your password!)"
echo "   Get token from: https://huggingface.co/settings/tokens"
echo ""

git push --force space main

echo ""
echo "✨ Deployment Complete! ✨"
echo "========================="
echo ""
echo "🌐 Your Space: ${HF_SPACE_URL}"
echo "📖 API Docs:   ${HF_SPACE_URL}/docs"
echo "🔍 Logs:       ${HF_SPACE_URL} (click 'Logs' tab)"
echo ""
echo "⏳ Build will take 5-10 minutes. Monitor progress in the Logs tab."
echo ""
echo "🧪 Test your API:"
echo "curl https://${HF_USERNAME}-${SPACE_NAME}.hf.space/"
echo ""
echo "Happy deploying! 🎉"

