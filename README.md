# Shopping Trends Intelligence

Python Project 2 interactive web application built with Streamlit, Plotly, pandas, and numpy.

The app converts the shopping trends analysis into an interactive dashboard with a landing page, grouped filters, reset controls, Plotly charts, and a dark Liquid Glass dashboard design inspired by the Open Design dashboard system.

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
- Liquid Glass / glassmorphism dashboard styling with subtle reveal and hover motion
- Reset button for all filters
- Grouped sidebar filters:
  - Customer
  - Product
  - Market
  - Transaction
- KPI cards
- Plotly charts for spending, customer behavior, products, locations, payment, shipping, discounts, promo use, and purchase frequency
- Filtered transaction explorer
