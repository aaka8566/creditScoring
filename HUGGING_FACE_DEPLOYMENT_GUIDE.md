# 🤗 Hugging Face Spaces Deployment Guide

Complete step-by-step guide to deploy your NBFC Credit Scoring API on Hugging Face Spaces.

## 📋 Prerequisites

1. **Hugging Face Account**: Create at [https://huggingface.co/join](https://huggingface.co/join)
2. **Git**: Installed on your system
3. **Git LFS**: For large model files

```bash
# Install Git LFS (if not already installed)
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Initialize Git LFS
git lfs install
```

---

## 🚀 Deployment Steps

### Step 1: Create a New Space

1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `nbfc-credit-scoring` (or your choice)
   - **License**: Apache 2.0 (recommended)
   - **SDK**: Select **Docker**
   - **Visibility**: Public or Private (your choice)
4. Click **"Create Space"**

### Step 2: Prepare Your Repository

```bash
# Navigate to your project directory
cd /Users/macbook/Desktop/dvaraRepos/scoring

# Initialize git (if not already initialized)
git init

# Copy the HF-specific README
cp README_HF.md README.md

# Use HF-specific requirements
cp requirements-hf.txt requirements.txt

# Track large model files with Git LFS
git lfs track "*.pkl"
git lfs track "*.bin"
git lfs track "*.pt"
git add .gitattributes
```

### Step 3: Add Your Files

```bash
# Add all necessary files
git add app.py
git add enhanced_main.py
git add enhanced_scoring.py
git add scoring.py
git add bank_statement_processor.py
git add Dockerfile
git add requirements.txt
git add README.md
git add xgb_model.pkl
git add label_encoder.pkl

# Commit changes
git commit -m "Initial commit for Hugging Face Spaces"
```

### Step 4: Connect to Hugging Face

```bash
# Add Hugging Face remote (replace USERNAME and SPACE_NAME)
git remote add space https://huggingface.co/spaces/USERNAME/SPACE_NAME

# For example:
# git remote add space https://huggingface.co/spaces/johndoe/nbfc-credit-scoring

# Push to Hugging Face
git push space main

# If you need to force push (first time)
git push --force space main
```

### Step 5: Authentication (if required)

If prompted for credentials:

1. **Username**: Your Hugging Face username
2. **Password**: Use a **Hugging Face Access Token** (not your password!)

**To create an access token:**
1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Name: `deployment-token`
4. Role: `write`
5. Click **"Generate a token"**
6. Copy the token and use it as password when pushing

**Store credentials (optional):**
```bash
git config --global credential.helper store
```

### Step 6: Monitor Build Progress

1. Go to your Space page: `https://huggingface.co/spaces/USERNAME/SPACE_NAME`
2. Click on **"Logs"** tab to see build progress
3. Wait for Docker build to complete (usually 5-10 minutes)
4. Status will change from 🔨 Building → ✅ Running

---

## 🔍 Testing Your Deployed API

Once deployed, your API will be available at:
```
https://USERNAME-SPACE_NAME.hf.space
```

### Test the Root Endpoint

```bash
curl https://USERNAME-SPACE_NAME.hf.space/
```

### Test Scoring Endpoint

```bash
curl -X POST "https://USERNAME-SPACE_NAME.hf.space/score" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "income": 50000,
    "loan_amount": 500000,
    "employment_type": "Salaried",
    "credit_score": 720,
    "existing_debt": 100000
  }'
```

### Access Interactive Documentation

Open in your browser:
- Swagger UI: `https://USERNAME-SPACE_NAME.hf.space/docs`
- ReDoc: `https://USERNAME-SPACE_NAME.hf.space/redoc`

---

## 🛠️ Updating Your Deployment

After making changes:

```bash
# Make your changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Update: description of changes"

# Push to Hugging Face
git push space main
```

The Space will automatically rebuild and redeploy.

---

## 🐛 Troubleshooting

### Issue: Build Fails

**Check logs:**
1. Go to Space → Logs tab
2. Look for error messages

**Common fixes:**
- Ensure all dependencies are in `requirements.txt`
- Check Dockerfile syntax
- Verify model files are committed

### Issue: Out of Memory

**Solution:** Request more resources
1. Go to Space Settings
2. Under "Hardware" select a better instance
3. Note: Better hardware requires HF Pro subscription

### Issue: App Not Responding

**Check:**
```bash
# Test health endpoint
curl https://USERNAME-SPACE_NAME.hf.space/health
```

**Common causes:**
- App crashed (check logs)
- Port mismatch (must be 7860)
- Startup timeout (increase in Dockerfile)

### Issue: Model Files Not Found

**Solution:**
```bash
# Track with Git LFS
git lfs track "*.pkl"
git add .gitattributes
git add xgb_model.pkl label_encoder.pkl
git commit -m "Add model files with LFS"
git push space main
```

---

## ⚙️ Configuration Options

### Environment Variables

Add in Space Settings → Variables:

```bash
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760  # 10MB
ENABLE_CORS=true
```

### Hardware Requirements

| Tier | CPU | RAM | Price |
|------|-----|-----|-------|
| Free | 2 vCPU | 16GB | Free |
| Basic | 2 vCPU | 16GB | $0/month |
| Pro | 8 vCPU | 32GB | $9/month |

For this app, **Free tier** should work fine!

---

## 🎨 Customization

### Update Space Appearance

Edit the header in `README.md`:

```yaml
---
title: Your Custom Title
emoji: 💰  # Choose any emoji
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---
```

### Add Custom Domain (Pro only)

1. Go to Space Settings
2. Under "Custom Domain"
3. Enter your domain
4. Follow DNS configuration instructions

---

## 📊 Space Analytics

View usage statistics:
1. Go to your Space
2. Click "Analytics" tab
3. See:
   - API calls per day
   - Response times
   - Error rates

---

## 🔒 Security Best Practices

### 1. Use Private Spaces for Sensitive Data

```bash
# Make space private
Settings → Visibility → Private
```

### 2. Add API Authentication

Update `enhanced_main.py`:

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

@app.post("/score", dependencies=[Depends(verify_token)])
def score_loan(application: LoanApplication):
    # ... your code
```

### 3. Rate Limiting

Add to `requirements.txt`:
```
slowapi==0.1.9
```

Update `enhanced_main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/score")
@limiter.limit("10/minute")
async def score_loan(request: Request, application: LoanApplication):
    # ... your code
```

---

## 📞 Getting Help

- **Hugging Face Forums**: [https://discuss.huggingface.co](https://discuss.huggingface.co)
- **Discord**: [https://discord.gg/huggingface](https://discord.gg/huggingface)
- **Documentation**: [https://huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)

---

## 🎉 Next Steps

After deployment:

1. ✅ Test all endpoints
2. ✅ Update README with your Space URL
3. ✅ Share on social media
4. ✅ Add to your portfolio
5. ✅ Monitor usage and errors
6. ✅ Collect feedback
7. ✅ Iterate and improve

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Hugging Face Spaces**: https://huggingface.co/docs/hub/spaces
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/

---

**Congratulations! 🎊** Your credit scoring API is now live on Hugging Face Spaces!

---

*Last updated: October 2025*

