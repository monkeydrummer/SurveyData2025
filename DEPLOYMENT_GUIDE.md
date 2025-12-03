# Quick Deployment Guide for Streamlit Cloud

## Deploy in 5 Minutes

### 1. Create GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it something like `survey-dashboard`
3. Keep it **Private** (recommended for internal tools)

### 2. Push Your Code

Open terminal in your project folder and run:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial survey dashboard"

# Add your GitHub repo (replace with your URL)
git remote add origin https://github.com/YOUR-USERNAME/survey-dashboard.git

# Push
git branch -M main
git push -u origin main
```

**✅ Your `.gitignore` file ensures the password is NOT uploaded to GitHub**

### 3. Deploy to Streamlit Cloud

1. **Go to:** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account

3. **Click** "New app" button

4. **Select:**
   - Repository: `YOUR-USERNAME/survey-dashboard`
   - Branch: `main`
   - Main file path: `app.py`

5. **Click** "Deploy"

### 4. Wait 2-3 Minutes

Streamlit will build and deploy your app. You'll get a URL like:
```
https://your-app-name.streamlit.app
```

### 5. Share the Link

Send the URL to your team:
- **URL:** `https://your-app-name.streamlit.app`

Users will need to upload their own CSV file when accessing the dashboard.

---

## Updating the Dashboard

After making changes to your code:

```bash
git add .
git commit -m "Updated dashboard"
git push
```

Streamlit Cloud will automatically redeploy!

---

## Troubleshooting

### App won't start
- Verify all files from `requirements.txt` are included
- Check the logs for specific error messages

### Need Help?
Check the logs on Streamlit Cloud by clicking on "Manage app" → "Logs"

### "Where's my data?"
The CSV file is NOT in the repository for privacy. Users must:
1. Log in with the password
2. Upload the CSV file using the sidebar file uploader
3. The dashboard will load once the file is uploaded

This keeps your survey data completely private!

---

## Privacy & Security

Your Streamlit Cloud app is public (anyone with the link can access it).

Security features:
- ✅ No sensitive data in the repository
- ✅ Users must upload their own CSV files
- ✅ Data is only stored in the user's session
- ✅ Data is never saved to the server

For additional security:
1. Don't share the app URL publicly if you want to restrict access
2. Consider using Streamlit Cloud's built-in authentication (paid feature) for enterprise use
3. Educate users to only upload the CSV when needed

---

## 🎉 You're Done!

Your survey dashboard is now live and accessible to your team!

