# 🎈 Deploying AI Analyst on Streamlit Community Cloud

Streamlit Community Cloud allows you to deploy Python apps directly from your GitHub repository for free in one click.

---

## 📋 Prerequisites
1. Code pushed to a public or private GitHub repository.
2. An account on [share.streamlit.io](https://share.streamlit.io/).
3. A **Groq API Key** from [Groq Console](https://console.groq.com/).

---

## 🚀 Deployment Guide

### Step 1: Sign in & Connect GitHub
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Sign in with your GitHub account.

### Step 2: Create a New App
1. Click the **"New app"** button in the top right corner.
2. Select your repository, branch (e.g. `main`), and specify main file path:
   - **Main file path**: `streamlit_app.py`

### Step 3: Configure Advanced Secrets (Groq API Key)
1. Before clicking Deploy, click **"Advanced settings..."**.
2. Under **Secrets**, enter your API key in TOML format:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
   ```
3. Click **Save**.

### Step 4: Deploy & Access
1. Click **Deploy!**.
2. Streamlit Cloud will install dependencies from `requirements.txt` and launch your dashboard.
3. Your app will be live at `https://<your-custom-subdomain>.streamlit.app`.

---

## 🎨 Theme Verification
Streamlit will automatically load the visual dark theme settings configured in [.streamlit/config.toml](file:///d:/LLMs_RAG/chatbot/.streamlit/config.toml).
