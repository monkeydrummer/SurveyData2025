# Survey Dashboard

A Streamlit dashboard for analyzing Rocscience Core Values Survey data with interactive visualizations, filtering, and data exploration capabilities.

## Features

- 📊 Interactive charts and heatmaps
- 🔍 Search and filter questions
- 📈 Department and tenure comparisons
- 🎯 Response grouping and "Don't Know" exclusion
- 📋 Detailed question-by-question analysis

## Local Development

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
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

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Sign in with GitHub

3. Click "New app"

4. Select your repository and branch

5. Set the main file path: `app.py`

6. Click "Deploy"

Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

## Usage

1. **Upload your survey CSV file** using the sidebar file uploader
2. Use sidebar filters to select departments and tenure groups
3. Toggle response grouping and "Don't Know" exclusion
4. Explore visualizations in Overview and Detailed Questions tabs
5. Use search to find specific questions
6. Sort heatmaps by different response types

**Note:** You'll need to upload the CSV file each time you start a new session.

## Data File

**Important:** Survey data is NOT stored in the repository for privacy.

- Users must upload the CSV file through the app interface
- The file uploader appears in the sidebar after logging in
- Supported format: Rocscience Core Values Survey CSV

## Support

For issues or questions, contact the dashboard administrator.

