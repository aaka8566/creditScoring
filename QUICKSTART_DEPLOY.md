# ⚡ Quick Start: Deploy to Hugging Face in 5 Minutes

The fastest way to get your credit scoring API live on Hugging Face Spaces.

## 🎯 Prerequisites Checklist

- [ ] Hugging Face account ([Sign up here](https://huggingface.co/join))
- [ ] Git installed (`git --version` to check)
- [ ] Git LFS installed (optional but recommended)

---

## 🚀 Deploy in 3 Steps

### Step 1: Create a Space on Hugging Face

1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Configure:
   - **Name**: `nbfc-credit-scoring` (or your choice)
   - **SDK**: Choose **Docker**
   - **Visibility**: Public or Private
4. Click **"Create Space"**

### Step 2: Run the Deployment Script

```bash
cd /Users/macbook/Desktop/dvaraRepos/scoring

# Make script executable
chmod +x deploy_to_hf.sh

# Run deployment
./deploy_to_hf.sh
```

The script will:
- ✅ Check dependencies
- ✅ Prepare deployment files
- ✅ Set up Git and Git LFS
- ✅ Push to Hugging Face

### Step 3: Get Your Access Token

When prompted for password, use an access token:

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Name: `deployment`
4. Role: **Write**
5. Click **"Generate"**
6. Copy token and paste when prompted

---

## 🎉 That's It!

Your API is deploying! 

### Monitor Progress

Visit your Space and click the **"Logs"** tab to watch the build.

**Build time**: ~5-10 minutes

### Access Your API

Once deployed:

```bash
# Test root endpoint
curl https://YOUR_USERNAME-SPACE_NAME.hf.space/

# Test scoring
curl -X POST "https://YOUR_USERNAME-SPACE_NAME.hf.space/score" \
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

### Interactive Documentation

Open in browser:
- 📖 Swagger UI: `https://YOUR_USERNAME-SPACE_NAME.hf.space/docs`
- 📘 ReDoc: `https://YOUR_USERNAME-SPACE_NAME.hf.space/redoc`

---

## 🛠️ Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# 1. Prepare files
cp README_HF.md README.md
cp requirements-hf.txt requirements.txt

# 2. Initialize git
git init
git checkout -b main

# 3. Set up Git LFS
git lfs install
git lfs track "*.pkl"

# 4. Add files
git add app.py Dockerfile requirements.txt README.md
git add enhanced_main.py enhanced_scoring.py scoring.py
git add bank_statement_processor.py
git add xgb_model.pkl label_encoder.pkl .gitattributes

# 5. Commit
git commit -m "Initial deployment"

# 6. Add Hugging Face remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE

# 7. Push
git push --force space main
```

---

## 🔥 Common Issues & Quick Fixes

### Issue: "Git LFS not installed"

**Fix:**
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Then
git lfs install
```

### Issue: "Authentication failed"

**Fix:** Use Access Token, not password!
- Get token from: https://huggingface.co/settings/tokens
- Select "Write" permission

### Issue: "Build failed"

**Fix:** Check logs in your Space's "Logs" tab
- Common cause: Missing dependencies
- Ensure all model files are committed

### Issue: "Space stuck in 'Building' state"

**Fix:** Wait 10 minutes, then:
1. Check logs for errors
2. If timeout, increase in Dockerfile:
   ```dockerfile
   HEALTHCHECK --start-period=60s ...
   ```

---

## 📞 Need Help?

1. **Full Guide**: Read `HUGGING_FACE_DEPLOYMENT_GUIDE.md`
2. **HF Forums**: [discuss.huggingface.co](https://discuss.huggingface.co)
3. **Discord**: [discord.gg/huggingface](https://discord.gg/huggingface)

---

## ✅ Post-Deployment Checklist

After successful deployment:

- [ ] Test all API endpoints
- [ ] Check interactive docs (`/docs`)
- [ ] Test with real data
- [ ] Update README with correct URLs
- [ ] Share your Space!
- [ ] Add to your portfolio

---

## 🎊 Success!

Your credit scoring API is now live and accessible worldwide! 🌍

Share it:
- Twitter/X: "Check out my AI credit scoring API on @huggingface Spaces!"
- LinkedIn: Add to your projects
- Portfolio: Link to your Space

---

**Time to deploy**: ~5 minutes  
**Time to build**: ~10 minutes  
**Total time**: ~15 minutes ⚡

Let's deploy! 🚀

