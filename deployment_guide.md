# 🚀 Deployment Guide for Stanford ETL RAG Chatbot

This guide covers multiple ways to host your RAG chatbot on a server.

## 📋 Prerequisites

1. **OpenAI API Key** with sufficient quota
2. **Transcript files** accessible to the server
3. **Git repository** with your code

## 🌐 Option 1: Streamlit Cloud (Recommended - Free)

### Steps:
1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/stanford-etl-chatbot.git
   git push -u origin main
   ```

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Configure Environment Variables:**
   - In your app settings, add:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `OPENAI_MODEL`: `gpt-4o` (or your preferred model)
     - `TRANSCRIPTS_DIR`: Path to your transcripts on the server

### Pros:
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Easy setup
- ✅ Built-in HTTPS

### Cons:
- ❌ Limited to Streamlit interface
- ❌ Need to upload transcripts separately

---

## 🐳 Option 2: Docker + Cloud Provider

### Create Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for transcripts
RUN mkdir -p /app/transcripts

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Deploy to Cloud Providers:

#### **A. Google Cloud Run:**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/stanford-etl-chatbot

# Deploy to Cloud Run
gcloud run deploy stanford-etl-chatbot \
  --image gcr.io/YOUR_PROJECT_ID/stanford-etl-chatbot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key,OPENAI_MODEL=gpt-4o
```

#### **B. AWS ECS/Fargate:**
```bash
# Build and push to Amazon ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker build -t stanford-etl-chatbot .
docker tag stanford-etl-chatbot:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/stanford-etl-chatbot:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/stanford-etl-chatbot:latest
```

#### **C. Azure Container Instances:**
```bash
# Build and push to Azure Container Registry
az acr build --registry YOUR_REGISTRY_NAME --image stanford-etl-chatbot .
```

---

## ☁️ Option 3: VPS/Cloud Server

### **A. DigitalOcean Droplet:**
```bash
# Connect to your droplet
ssh root@your_server_ip

# Install dependencies
apt update
apt install -y python3 python3-pip git nginx

# Clone your repository
git clone https://github.com/yourusername/stanford-etl-chatbot.git
cd stanford-etl-chatbot

# Install Python dependencies
pip3 install -r requirements.txt

# Create environment file
nano .env
# Add your OpenAI API key

# Upload transcripts
scp -r /path/to/transcripts root@your_server_ip:/root/stanford-etl-chatbot/

# Run with systemd service
sudo nano /etc/systemd/system/stanford-chatbot.service
```

**Systemd service file:**
```ini
[Unit]
Description=Stanford ETL Chatbot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/stanford-etl-chatbot
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/local/bin/streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable stanford-chatbot
sudo systemctl start stanford-chatbot

# Configure Nginx
sudo nano /etc/nginx/sites-available/stanford-chatbot
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

```bash
# Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/stanford-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **B. AWS EC2:**
```bash
# Launch EC2 instance (Ubuntu recommended)
# Connect via SSH
ssh -i your-key.pem ubuntu@your-instance-ip

# Follow similar steps as DigitalOcean
# Use AWS CLI for additional services
```

---

## 🔧 Option 4: Serverless (Advanced)

### **AWS Lambda + API Gateway:**
1. Create Lambda function with your chatbot logic
2. Set up API Gateway for HTTP endpoints
3. Use S3 for transcript storage
4. Configure environment variables

### **Google Cloud Functions:**
1. Deploy as Cloud Function
2. Use Cloud Storage for transcripts
3. Set up Cloud Run for the web interface

---

## 📁 Handling Transcripts in Production

### **Option A: Include in Docker Image (Small datasets)**
```dockerfile
COPY transcripts/ /app/transcripts/
```

### **Option B: Cloud Storage (Recommended)**
```python
# Modify transcript_loader.py to support cloud storage
import boto3  # For AWS S3
# or
from google.cloud import storage  # For Google Cloud Storage
```

### **Option C: Database Storage**
```python
# Store transcript chunks in PostgreSQL/MongoDB
# Use vector extensions for similarity search
```

---

## 🔐 Security Considerations

1. **Environment Variables:** Never commit API keys to Git
2. **HTTPS:** Always use HTTPS in production
3. **Rate Limiting:** Implement rate limiting for API calls
4. **Authentication:** Add user authentication if needed
5. **CORS:** Configure CORS properly for web apps

---

## 📊 Monitoring & Logging

### **Add logging to your app:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add to your chatbot
logger.info(f"Processing query: {query}")
```

### **Health checks:**
```python
# Add health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy'}
```

---

## 💰 Cost Estimation

- **Streamlit Cloud:** Free tier available
- **Cloud Run:** ~$5-20/month for moderate usage
- **VPS:** $5-20/month (DigitalOcean, Linode)
- **EC2:** $10-50/month depending on instance
- **OpenAI API:** $0.01-0.10 per query

---

## 🚀 Quick Start Recommendation

1. **Start with Streamlit Cloud** (easiest)
2. **Move to Docker + Cloud Run** when you need more control
3. **Consider VPS** for full control and custom domains

Choose based on your technical expertise and budget! 