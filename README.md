# ◈ NEXA Feedback Platform

A beautiful, NEXA-branded multi-step feedback form with a password-protected admin dashboard — built with Streamlit.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

**Feedback Form (Home page)**
- 4-step guided form with progress bar
- Module selection, star rating, emoji satisfaction picker, sliders
- Validates inputs before proceeding
- Saves every response to `data/responses.csv`
- Unique response ID per submission

**Admin Dashboard (`/Admin_Dashboard`)**
- Password-protected login
- Live stats: total responses, avg rating, recommendation %, ease score
- Searchable response table + full detail view per response
- Analytics charts: ratings, satisfaction, modules, roles, sources
- Export to CSV (Excel) or JSON
- Import from exported files (merge across devices)
- Delete all responses with confirmation

---

## 📁 Project Structure

```
nexa-feedback/
├── Home.py                        # Feedback form (main page)
├── pages/
│   └── 1_Admin_Dashboard.py       # Admin dashboard
├── data/
│   ├── .gitkeep
│   └── responses.csv              # Auto-created on first submission
├── .streamlit/
│   ├── config.toml                # Theme & server config
│   └── secrets.toml.example       # Template — copy & fill in
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Deploy on Streamlit Cloud (Recommended — Free)

### Step 1 — Push to GitHub

```bash
# In your terminal
cd nexa-feedback
git init
git add .
git commit -m "Initial commit — NEXA Feedback App"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/nexa-feedback.git
git branch -M main
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** → Sign in with GitHub
2. Click **"New app"**
3. Select your repo: `nexa-feedback`
4. Main file path: `Home.py`
5. Click **"Advanced settings"** → Add secret:
   ```
   ADMIN_PASSWORD = "your_strong_password"
   ```
6. Click **Deploy** ✅

Your app will be live at:
- **Form:** `https://your-app-name.streamlit.app`
- **Admin:** `https://your-app-name.streamlit.app/Admin_Dashboard`

> ⚠️ **Important:** Streamlit Cloud's free tier has ephemeral storage. Responses saved to `data/responses.csv` will reset if the app restarts. See [Persistent Storage](#-persistent-storage) below.

---

## 💻 Run Locally

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/nexa-feedback.git
cd nexa-feedback

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Set up your admin password
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and set your password

# Run the app
streamlit run Home.py
```

Open **http://localhost:8501** in your browser.

---

## 🔐 Admin Access

The admin dashboard is password-protected.

**Default password:** `nexa2024` (change this before deploying!)

To change the password:
- **Locally:** Edit `.streamlit/secrets.toml`
- **Streamlit Cloud:** Go to App Settings → Secrets → update `ADMIN_PASSWORD`

---

## 💾 Persistent Storage

On Streamlit Cloud's free tier, the filesystem resets on restart. To keep responses permanently, use one of these:

### Option A — Google Sheets (Easiest)
Install `gspread` and write responses to a Google Sheet.

```bash
pip install gspread google-auth
```

### Option B — Supabase (Free PostgreSQL)
```bash
pip install supabase
```
Replace the `save_response()` function in `Home.py` to insert into Supabase.

### Option C — GitHub (Auto-commit responses)
Use GitHub Actions to commit `responses.csv` after each submission.

### Option D — Download regularly
Use the **Export CSV** button in the admin dashboard to download responses before the app restarts.

---

## 📊 Accessing Your Data

All responses are stored in `data/responses.csv` with these columns:

| Column | Description |
|--------|-------------|
| `id` | Unique response ID (e.g. NX-A1B2C3D4) |
| `timestamp` | Date and time of submission |
| `name` | Respondent's full name |
| `email` | Email address |
| `role` | Occupation / role |
| `usage_duration` | How long they've used NEXA |
| `modules_used` | Comma-separated list of modules tried |
| `overall_rating` | Star rating (1–5) |
| `ease_of_use` | Ease score (1–10) |
| `satisfaction` | Satisfaction level (emoji label) |
| `best_thing` | What they loved most |
| `improvement` | What needs to improve |
| `recommend` | Would they recommend NEXA? |
| `feature_request` | Feature ideas |
| `message` | Free-form message to the team |
| `source` | How they found NEXA |

---

## 🛠 Local Development Tips

```bash
# Auto-reload on file changes (default behaviour)
streamlit run Home.py

# Run on a specific port
streamlit run Home.py --server.port 8502

# Clear Streamlit cache
streamlit cache clear
```

---

## 📦 Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
```

---

## 📄 License

MIT — free to use and modify.

---

Built with ❤️ for the **NEXA Unified AI Platform**
