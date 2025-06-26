# 🚀 Streamlit Cloud Deployment Guide

## Quick Setup for Streamlit Cloud

### 1. Prepare Your Repository
- ✅ All files are already in your repository
- ✅ Large files (chroma_db) are excluded from Git
- ✅ Requirements.txt is properly configured

### 2. Deploy to Streamlit Cloud

1. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app:**
   - Repository: `yourusername/stanford_etl_chatbot`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

### 3. Configure Environment Variables

In your Streamlit Cloud app settings, add these secrets:

```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
OPENAI_MODEL = "gpt-4o"
TRANSCRIPTS_DIR = "/app/transcripts"
```

### 4. Upload Transcripts (Required)

**Option A: Include in Repository (Recommended for small datasets)**
```bash
# Create transcripts directory in your repo
mkdir transcripts
# Copy your transcript files to this directory
cp /path/to/your/transcripts/*.txt transcripts/
# Commit and push
git add transcripts/
git commit -m "Add transcript files"
git push
```

**Option B: Use Cloud Storage**
- Upload transcripts to Google Drive, Dropbox, or similar
- Modify the app to download from cloud storage
- Set up automatic download on app startup

### 5. Common Issues & Solutions

#### Issue: "ImportError: No module named 'rag_chatbot'"
**Solution:** All required files are in the repository. This shouldn't happen.

#### Issue: "Transcripts directory not found"
**Solution:** 
- Upload transcript files to the repository
- Or set up cloud storage for transcripts

#### Issue: "OPENAI_API_KEY not found"
**Solution:**
- Add your API key to Streamlit Cloud secrets
- Make sure to use the new API key (not the exposed one)

#### Issue: "Vector store not found"
**Solution:**
- The app will automatically create the vector store
- Click "Setup Vector Store" in the sidebar

### 6. Testing Your Deployment

1. **Check the app loads** without errors
2. **Click "Setup Vector Store"** in the sidebar
3. **Try asking a question** like "What advice do entrepreneurs give about starting a company?"
4. **Check the logs** if there are any issues

### 7. Performance Tips

- **First run will be slow** as it processes all transcripts
- **Subsequent runs will be faster** with the built vector store
- **Consider using a smaller model** like `gpt-3.5-turbo` for faster responses

### 8. Security Notes

- ✅ Never commit API keys to Git
- ✅ Use Streamlit Cloud secrets for sensitive data
- ✅ Keep your repository private until API key is rotated
- ✅ Rotate your API key if it was ever exposed

## 🎉 You're Ready!

Once deployed, your RAG chatbot will be available at:
`https://your-app-name.streamlit.app` 