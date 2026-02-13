# Pulse — Interactive Feedback System

A dark-themed, production-grade Streamlit feedback system with real-time analytics.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run feedback_app.py
```

Then open **http://localhost:8501** in your browser.

---

## Features

| Page | What it does |
|------|-------------|
| **Submit Feedback** | Multi-field form: name, email, category, rating (1–5 stars), free text, tags, NPS score |
| **Dashboard** | Rating distribution, sentiment pie chart, time-series area chart, category & source breakdowns |
| **Response Manager** | Browse, filter, and reply to all submitted feedback |
| **Settings** | Export data as CSV or JSON, clear all data |

## Data Storage
Feedback is saved locally to `feedback_data.json` in the same directory.

## Tech Stack
- **Streamlit** — UI framework
- **Plotly** — interactive charts
- **Pandas** — data manipulation
- **DM Serif Display / DM Mono / DM Sans** — Google Fonts
