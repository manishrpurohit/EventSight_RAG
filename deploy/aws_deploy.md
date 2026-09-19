# ☁️ Deploying AI Analyst on AWS (Amazon Web Services)

This guide provides step-by-step instructions for deploying the **AI Analyst** app on AWS using two production deployment architectures:
1. **AWS App Runner** (Fully managed serverless container service - Recommended)
2. **AWS EC2 with Docker Compose** (Virtual Machine with Docker orchestrator)

---

## Option 1: Deploy on AWS App Runner (Serverless Container - Recommended)

AWS App Runner makes it easy to deploy containerized web applications at scale with automatic load balancing and SSL.

### Step 1: Push Container Image to AWS ECR (Elastic Container Registry)

1. **Log in to AWS CLI**:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   ```

2. **Create ECR Repository**:
   ```bash
   aws ecr create-repository --repository-name ai-analyst
   ```

3. **Build & Tag Docker Image**:
   ```bash
   docker build -t ai-analyst .
   docker tag ai-analyst:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-analyst:latest
   ```

4. **Push Image to ECR**:
   ```bash
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-analyst:latest
   ```

### Step 2: Create AWS App Runner Service

1. Open **AWS App Runner Console** and click **Create service**.
2. **Source**: Select **Container registry** -> **Amazon ECR**.
3. **Image URI**: Select `<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-analyst:latest`.
4. **Deployment Trigger**: Select **Automatic** (re-deploys when new Docker image is pushed).
5. **Configure Service**:
   - **Service Name**: `ai-analyst-service`
   - **Port**: `8501`
   - **Environment Variables**:
     - Key: `GROQ_API_KEY`, Value: `your_groq_api_key`
     - Key: `PORT`, Value: `8501`
6. Click **Create & Deploy**. AWS App Runner will issue an HTTPS URL (e.g. `https://xxx.us-east-1.awsapprunner.com`).

---

## Option 2: Deploy on AWS EC2 (Elastic Compute Cloud)

Deploy on an Ubuntu EC2 instance using Docker & Docker Compose.

### Step 1: Launch EC2 Instance
1. Launch an **Ubuntu 22.04 LTS** EC2 instance (`t3.medium` or `t2.medium` recommended).
2. Configure **Security Group** inbound rules:
   - Port 22 (SSH)
   - Port 8501 (Streamlit UI)
   - Port 7860 (Gradio UI - optional)
   - Port 80 / 443 (HTTP/HTTPS)

### Step 2: SSH into EC2 & Install Docker
```bash
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com

# Update packages and install Docker
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose git

# Enable Docker without sudo
sudo usermod -aG docker ubuntu
newgrp docker
```

### Step 3: Clone Repository & Launch Containers
```bash
# Clone repository
git clone https://github.com/your-username/chatbot.git
cd chatbot

# Create .env file with your API key
echo "GROQ_API_KEY=your_actual_groq_key_here" > .env

# Run containers in detached mode
docker-compose up -d --build
```

### Step 4: Verify Live App
Access Streamlit at `http://<YOUR_EC2_PUBLIC_IP>:8501` and Gradio at `http://<YOUR_EC2_PUBLIC_IP>:7860`.
