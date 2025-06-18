# Deployment Guide for Streamlit Community

This guide will help you deploy the Twelve Labs Video Uploader to Streamlit Community Cloud.

## 📋 Prerequisites

1. **GitHub Account**: You'll need a GitHub account to host your code
2. **Streamlit Community Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Twelve Labs API Key**: Get your API key from [Twelve Labs Console](https://playground.twelvelabs.io/)

## 🚀 Step-by-Step Deployment

### Step 1: Push to GitHub

1. **Create a new repository** on GitHub:
   - Go to [GitHub](https://github.com) and click "New repository"
   - Name it something like `twelve-labs-video-uploader`
   - Make it **public** (required for Streamlit Community)
   - Don't initialize with README (we already have one)

2. **Push your code** to GitHub:
   ```bash
   cd /path/to/your/project
   git init
   git add .
   git commit -m "Initial commit: Twelve Labs Video Uploader"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/twelve-labs-video-uploader.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Community

1. **Go to Streamlit Community**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create new app**:
   - Click "New app"
   - Choose your repository: `YOUR_USERNAME/twelve-labs-video-uploader`
   - Branch: `main`
   - Main file path: `app.py`
   - Choose a custom URL (optional): `your-app-name`

3. **Add secrets**:
   - Click on "Advanced settings" before deploying
   - In the "Secrets" section, add:
   ```toml
   TWELVE_LABS_API_KEY = "your_actual_api_key_here"
   ```

4. **Deploy**:
   - Click "Deploy!"
   - Wait for the deployment to complete (usually 2-3 minutes)

### Step 3: Test Your Deployment

1. **Access your app**:
   - Your app will be available at: `https://your-app-name.streamlit.app`
   - Or the auto-generated URL provided by Streamlit

2. **Test functionality**:
   - Upload a small video file first
   - Try creating a new index
   - Test with a video longer than 1 hour to verify chunking works

## 🔧 Configuration Files

These files are essential for deployment:

### `requirements.txt`
All Python dependencies are listed here. Streamlit Community will automatically install them.

### `packages.txt`
Contains system packages (like `ffmpeg`) that need to be installed on the deployment server.

### `.streamlit/config.toml`
Streamlit configuration for large file uploads. This allows the app to handle files up to 100GB.

## 🐛 Troubleshooting

### Common Issues:

**1. FFmpeg not found**
- Make sure `packages.txt` contains `ffmpeg`
- If issues persist, add these to `packages.txt`:
  ```
  ffmpeg
  libsm6
  libxext6
  ```

**2. Large file uploads failing**
- Ensure `.streamlit/config.toml` is properly configured
- The maxUploadSize should be set to 102400 (100GB)

**3. API key issues**
- Make sure your API key is added to Streamlit secrets
- The key should be valid and have proper permissions

**4. Memory issues with large videos**
- The chunking algorithm processes videos in segments to avoid memory issues
- Very large files (>50GB) might still cause timeouts

### Deployment Logs:

To view deployment logs:
1. Go to your app on Streamlit Community
2. Click the hamburger menu (≡) in the top right
3. Select "Manage app"
4. View logs under the "Logs" tab

## 🔄 Updates and Maintenance

### Updating Your App:

1. Make changes to your local code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. Streamlit Community will automatically redeploy your app

### Managing Secrets:

To update your API key or add new secrets:
1. Go to your app settings on Streamlit Community
2. Navigate to "Secrets"
3. Update the values and save
4. The app will automatically restart with new secrets

## 📊 App Limits

### Streamlit Community Limits:
- **Storage**: 1GB persistent storage
- **Memory**: 1GB RAM
- **CPU**: Shared CPU resources
- **Bandwidth**: Fair usage policy

### Twelve Labs API Limits:
- Check your plan limits on the Twelve Labs Console
- Monitor your API usage to avoid hitting limits

## 🌟 Best Practices

1. **Error Handling**: The app includes comprehensive error handling for production use
2. **Resource Cleanup**: Temporary files are automatically cleaned up
3. **User Feedback**: Clear progress indicators and error messages
4. **Security**: API keys are handled securely through Streamlit secrets

## 📞 Support

If you encounter issues:

1. **Check deployment logs** first
2. **Review this guide** for common solutions
3. **Create an issue** on your GitHub repository
4. **Contact Streamlit Community** support if needed

## 🎉 Success!

Once deployed, your app will be publicly accessible and ready to use. Share the URL with others who need to upload videos to Twelve Labs indexes!

**Example URL**: `https://twelve-labs-video-uploader.streamlit.app`

---

Happy deploying! 🚀
