# 🚀 Deploying AI Analyst on Render

Render is a unified cloud platform for building and running apps and sites. Follow this step-by-step guide to deploy your **AI Analyst** app on Render.

---

## 📋 Prerequisites
1. A **GitHub** account with this repository pushed.
2. A free account on **[Render.com](https://render.com/)**.
3. A **Groq API Key** from [Groq Console](https://console.groq.com/).

---

## 🛠️ Deployment Steps

### Method 1: Render Blueprint (Automated - Recommended)

1. **Push your code to GitHub**:
   Ensure your latest commits with `render.yaml` are pushed to your GitHub repository.

2. **Connect to Render**:
   - Log into [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** in the top right and select **Blueprints**.
   - Connect your GitHub repository.

3. **Configure Environment Variables**:
   - Render will read `render.yaml` and auto-configure `ai-analyst-streamlit`.
   - When prompted for `GROQ_API_KEY`, enter your Groq API Key value (e.g. `gsk_...`).

4. **Deploy**:
   - Click **Apply**. Render will automatically pull the code, install dependencies from `requirements.txt`, and start the app.
   - Access your live app at `https://ai-analyst-streamlit.onrender.com`.

---

### Method 2: Manual Web Service Creation (Python Environment)

1. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Fill in the deployment details:
   - **Name**: `ai-analyst`
   - **Language**: `Python 3`
   - **Branch**: `main` (or your active branch)
   - **Region**: Select nearest region (e.g., Singapore / Oregon / Frankfurt)
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
4. Under **Environment Variables**:
   - Key: `GROQ_API_KEY`, Value: `your_actual_groq_key`
   - Key: `PYTHON_VERSION`, Value: `3.10.12`
5. Click **Create Web Service**.

---

### Method 3: Containerized Deployment (Docker)

1. Select **New +** -> **Web Service** on Render.
2. Choose **Existing Image** or connect your Git repository with Docker environment:
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
3. Add `GROQ_API_KEY` under Environment Variables.
4. Render will build and run your Docker container automatically.

---

## 🔍 Health Check & Troubleshooting

- **Health Check Path**: Render will automatically check `/_stcore/health` for Streamlit.
- **Memory Optimization**: If running on Render free tier (512MB RAM), the `faiss-cpu` and `MiniLM-L6-v2` models are optimized to consume <300MB RAM.
