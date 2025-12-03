# Quick Deployment Guide for Streamlit Cloud

## Your Dashboard Password

```
RocSci2024!Survey#Dash$92
```

**Keep this password secure!**

---

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

5. **Click** "Advanced settings"

6. **In the Secrets section**, paste:
   ```toml
   password = "RocSci2024!Survey#Dash$92"
   ```

7. **Click** "Deploy"

### 4. Wait 2-3 Minutes

Streamlit will build and deploy your app. You'll get a URL like:
```
https://your-app-name.streamlit.app
```

### 5. Share the Link

Send the URL and password to your team:
- **URL:** `https://your-app-name.streamlit.app`
- **Password:** `RocSci2024!Survey#Dash$92`

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

## Changing the Password

### On Streamlit Cloud:
1. Go to your app at [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. Click ⚙️ Settings
4. Go to "Secrets"
5. Update the password line
6. Click "Save"
7. App will restart with new password

### Locally:
Edit `.streamlit/secrets.toml` and change the password line.

---

## Troubleshooting

### "Password incorrect" on Streamlit Cloud
- Make sure you added the password in the Secrets section (step 3.6 above)
- Check for extra spaces or quotes in the password

### App won't start
- Check that `Rocscience Core Values Survey 2.csv` is in your repository
- Verify all files from `requirements.txt` are included

### Need Help?
Check the logs on Streamlit Cloud by clicking on "Manage app" → "Logs"

### "Where's my data?"
The CSV file is NOT in the repository for privacy. Users must:
1. Log in with the password
2. Upload the CSV file using the sidebar file uploader
3. The dashboard will load once the file is uploaded

This keeps your survey data completely private!

---

## Making It Private

Your Streamlit Cloud app is public by default (anyone with the link can access it).
The password provides access control.

For additional security:
1. Keep your GitHub repo private
2. Don't share the app URL publicly
3. Change the password periodically
4. Use Streamlit Cloud's built-in authentication (paid feature) for enterprise use

---

## 🎉 You're Done!

Your survey dashboard is now live and accessible to your team!

