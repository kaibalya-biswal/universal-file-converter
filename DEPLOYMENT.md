# Deployment Guide

This Flask application can be deployed to various platforms. Here are the recommended options:

## Quick Deploy Options

### 1. **Railway** (Recommended - Easiest)
- Go to [railway.app](https://railway.app)
- Sign up/login with GitHub
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository
- Railway will automatically detect Flask and deploy
- Your app will be live in minutes!

### 2. **Render**
- Go to [render.com](https://render.com)
- Sign up/login with GitHub
- Click "New" → "Web Service"
- Connect your GitHub repository
- Settings:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app`
- Click "Create Web Service"

### 3. **Heroku**
- Install Heroku CLI
- Login: `heroku login`
- Create app: `heroku create your-app-name`
- Deploy: `git push heroku main`
- Open: `heroku open`

### 4. **PythonAnywhere**
- Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
- Upload your files via Files tab
- Configure Web app in Web tab
- Set WSGI file to point to your app

## Environment Variables

No environment variables are required for basic deployment. The app will:
- Use PORT from environment (or default to 5000)
- Create uploads/ and outputs/ folders automatically
- Run in production mode (debug=False) by default

## Important Notes

1. **File Storage**: Uploaded files are stored temporarily and deleted after 1 hour
2. **File Size Limit**: Maximum 16MB per file
3. **Dependencies**: All required packages are in `requirements.txt`
4. **Static Files**: CSS, JS, and templates are included in the repository

## Post-Deployment

After deployment, your app will be accessible at:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Heroku: `https://your-app-name.herokuapp.com`

## Troubleshooting

- If uploads fail, ensure the platform allows file system writes
- Some platforms may require additional configuration for file handling
- Check platform logs if the app doesn't start
