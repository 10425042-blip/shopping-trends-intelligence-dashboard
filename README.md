# Shopping Trends Intelligence

Interactive retail analytics dashboard built with Streamlit, Plotly, and pandas.

The app converts the shopping trends dataset into a focused presentation dashboard with a landing page, grouped global filters, reset controls, curated Plotly charts, concise chart captions, and a dark glassmorphism dashboard design.

The checked-in data file is the provided `shopping_trends_updated (2).csv` dataset, saved as `data/shopping_trends.csv` for Streamlit deployment.

## Run Locally

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

## Streamlit Cloud

Deploy from a GitHub repository with `streamlit_app.py` selected as the main file. Keep these files in the repo:

- `streamlit_app.py`
- `requirements.txt`
- `data/shopping_trends.csv`
- `.streamlit/config.toml`

No secrets are required for this project. The legacy Dash files are not part of the Streamlit deployment package.

In Streamlit Community Cloud, use Python 3.12 in Advanced settings if a Python version is requested. Community Cloud currently defaults to Python 3.12, which matches the local virtual environment used for this app.

## Dashboard Features

- Landing page with a retail background and Explore Dashboard button
- Dark glassmorphism dashboard styling without custom animation rules
- Reset button for all filters
- Grouped sidebar filters:
  - Customer
  - Product
  - Market
  - Transaction
- KPI cards
- Four focused dashboard views for overview, customer insights, product sales, and data exploration
- Plotly charts for revenue share, seasonal revenue pulse, subscription gauge, customer value matrix, product demand mapping, and category-season performance
- Filtered transaction explorer
