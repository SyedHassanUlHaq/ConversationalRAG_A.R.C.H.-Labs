# 🚀 Deployment Guide for A.R.C.H. Labs Customer Support RAG System

## 🎯 **Overview**

Your customer support RAG system needs to be deployed to a public URL before integrating with your live portfolio website. Here are the best **FREE** deployment options:

## 🏆 **Recommended: Railway (Free)**

### **Why Railway?**
- ✅ **Always free** for hobby projects
- ✅ **Automatic deployments** from Git
- ✅ **Built-in environment variables**
- ✅ **Fast deployment** (< 5 minutes)
- ✅ **Custom domains** supported

### **Railway Deployment Steps:**

1. **Create Railway Account**
   - Go to: https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your RAG project repository
   - Railway will auto-detect Python and use `Procfile`

3. **Set Environment Variables**
   - Go to project → Variables tab
   - Add: `GOOGLE_API_KEY=your_google_ai_key`
   - Add: `OPENAI_API_KEY=your_openai_key` (if using)

4. **Get Your URL**
   - Railway will provide a URL like: `https://your-app-name.railway.app`
   - This is your RAG system URL!

---

## 🌟 **Alternative: Render (Free)**

### **Why Render?**
- ✅ **Free tier** with 750 hours/month
- ✅ **Automatic SSL** certificates
- ✅ **Git integration**
- ✅ **Custom domains**

### **Render Deployment Steps:**

1. **Create Render Account**
   - Go to: https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `chainlit run chainlit_app_free.py --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   - Add `GOOGLE_API_KEY` and `OPENAI_API_KEY`

4. **Deploy**
   - Render will give you a URL like: `https://your-app.onrender.com`

---

## ⚡ **Alternative: Heroku (Free with verification)**

### **Heroku Deployment Steps:**

1. **Install Heroku CLI**
   ```bash
   # On your local machine
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create arch-labs-support
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your_google_ai_key
   heroku config:set OPENAI_API_KEY=your_openai_key
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy RAG system"
   git push heroku main
   ```

---

## 🔧 **Local Testing Before Deployment**

Before deploying, test that your system works with environment variables:

```bash
# Test your current setup
python test_google_free.py

# Make sure chainlit runs properly
chainlit run chainlit_app_free.py --host 0.0.0.0 --port 8000
```

## 🌐 **After Deployment**

1. **Get your deployed URL** (e.g., `https://your-app.railway.app`)
2. **Test the deployed system** by visiting the URL
3. **Update the widget iframe** with your deployed URL
4. **Integrate widget** into your portfolio website

---

## 🚨 **Important Notes**

### **Environment Variables Required:**
- `GOOGLE_API_KEY` - Your Google AI API key
- `OPENAI_API_KEY` - Your OpenAI API key (if using)

### **Files Needed for Deployment:**
- ✅ `Procfile` - For Railway/Heroku
- ✅ `railway.json` - For Railway configuration
- ✅ `render.yaml` - For Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `.env.example` - Environment template

### **Port Configuration:**
All deployment configs use `$PORT` environment variable which hosting platforms provide automatically.

---

## 📞 **Need Help?**

If you encounter any deployment issues:
1. Check the deployment logs in your hosting platform
2. Verify environment variables are set correctly
3. Ensure all dependencies are in `requirements.txt`

**Contact for support:**
- Email: ahsantoufiq@archlabs.tech
- Phone: +923121359857

---

## 🎯 **Next Steps**

1. **Choose a deployment platform** (Railway recommended)
2. **Deploy your RAG system**
3. **Get your public URL**
4. **Proceed with portfolio integration**

Once deployed, we'll integrate the widget into your portfolio website! 