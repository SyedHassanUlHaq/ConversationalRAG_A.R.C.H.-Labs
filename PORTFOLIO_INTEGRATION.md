# 🎯 Portfolio Integration Guide

## 🚀 **Step 1: Deploy RAG System**

**Deploy your RAG system first to get a public URL.**

### Railway (Recommended):
1. Push code to GitHub
2. Go to https://railway.app → Deploy from GitHub
3. Set environment variables: `GOOGLE_API_KEY`
4. Get your URL: `https://your-app.railway.app`

## 📝 **Step 2: Integration Code**

### **Add to your portfolio's index.html:**

**In `<head>` section:**
```html
<!-- A.R.C.H. Labs Support Widget -->
<link rel="stylesheet" href="widget/support-widget.css">
```

**Before closing `</body>`:**
```html
<!-- A.R.C.H. Labs Support Widget -->
<script src="widget/support-widget.js"></script>
```

## 🔧 **Step 3: Update Configuration**

**Edit `widget/support-widget.js`:**
```javascript
const CHATBOT_URL = 'https://your-deployed-url.railway.app'; // Your actual URL
```

## 📁 **Step 4: Copy Files**

```bash
# Navigate to portfolio
cd /home/ahsantoufiq/Documents/A.R.C.H._Web

# Create widget directory
mkdir widget

# Copy files
cp ../Langchain\ Conversational\ RAG\ -\ ARCH\ Labs/portfolio-integration/support-widget.css widget/
cp ../Langchain\ Conversational\ RAG\ -\ ARCH\ Labs/portfolio-integration/support-widget.js widget/
```

## 🧪 **Step 5: Test & Deploy**

```bash
# Test locally
python -m http.server 3001

# Deploy to live site
git add .
git commit -m "Add customer support widget"
git push origin master
```

**🎉 Your portfolio now has AI customer support!** 