# Survey Dashboard

A Streamlit dashboard for analyzing Rocscience Core Values Survey data with interactive visualizations, filtering, and data exploration capabilities.

## Features

- 📊 Interactive charts and heatmaps
- 🔍 Search and filter questions
- 📈 Department and tenure comparisons
- 🎯 Response grouping and "Don't Know" exclusion
- 🔐 Password protected access
- 📋 Detailed question-by-question analysis

## Local Development

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.streamlit/secrets.toml` (already created):
```toml
password = "your-password-here"
```

3. Run the app:
```bash
streamlit run app.py --server.port 5621
```

## Deploying to Streamlit Cloud

### Step 1: Push to GitHub

1. Initialize git (if not already):
```bash
git init
git add .
git commit -m "Initial commit"
```

2. Create a new repository on GitHub

3. Push your code:
```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git branch -M main
git push -u origin main
```

**Important:** The `.gitignore` file ensures your `secrets.toml` is NOT pushed to GitHub.

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Sign in with GitHub

3. Click "New app"

4. Select your repository and branch

5. Set the main file path: `app.py`

6. Click "Advanced settings" and add secrets:
   - In the "Secrets" section, paste:
   ```toml
   password = "RocSci2024!Survey#Dash$92"
   ```

7. Click "Deploy"

Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

## Current Password

**Password:** `RocSci2024!Survey#Dash$92`

⚠️ **Security Note:** Change this password after first deployment by:
- Locally: Edit `.streamlit/secrets.toml`
- On Streamlit Cloud: Update in app settings → Secrets

## Usage

1. Enter the password to access the dashboard
2. Use sidebar filters to select departments and tenure groups
3. Toggle response grouping and "Don't Know" exclusion
4. Explore visualizations in Overview and Detailed Questions tabs
5. Use search to find specific questions
6. Sort heatmaps by different response types
7. Click "Logout" to exit

## Data File

Place your survey data file in the root directory:
- `Rocscience Core Values Survey 2.csv`

## Support

For issues or questions, contact the dashboard administrator.

