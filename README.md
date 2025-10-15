COVID-19 Data Pipeline Project

Full-stack Project: Python (Flask) backend + HTML/CSS/JS frontend
Dataset: Daily COVID-19 cases in India

Project Structure
covid_pipeline_project/
│
├── backend/
│   ├── app.py                 # Flask backend
│   ├── requirements.txt       # Python dependencies
│   └── data/
│       └── cleaned_covid_data_india.csv  # Sample CSV dataset
│
├── frontend/
│   ├── index.html             # Dashboard UI
│   ├── style.css              # Styles for frontend
│   └── script.js              # JS for charts, table, and interaction
│
└── README.md                  # Project documentation

Features

Table of daily COVID-19 cases

Interactive line chart of new cases (Chart.js)

Date range filter, search, sorting, pagination

Export visible data to CSV

Dark mode toggle

Summary stats (latest total + average new cases)

Frontend

HTML/CSS/JS files under frontend/

Uses Chart.js for line chart

Interactive controls:

Date range filter

Location search

Sorting by columns

Pagination

CSV export

Dark mode toggle

Backend

Flask app under backend/

Endpoints:

GET /api/get-data — retrieve filtered, sorted, paginated COVID data

GET /api/stats — summary stats (latest total cases, average new cases/day)

Loads CSV file: backend/data/cleaned_covid_data_india.csv

Note: Flask backend serves frontend as well.

How to Run Locally
1. Clone the repository
git clone https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git
cd covid_pipeline_project

2. Create a virtual environment
python -m venv venv

3. Activate the virtual environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

4. Install backend dependencies
pip install -r backend/requirements.txt

5. Run the Flask backend
python backend/app.py


Server will start at http://localhost:5000.

Backend also serves frontend automatically.

6. Open the frontend

Open in browser:

http://localhost:5000


You will see the dashboard with table, chart, filters, CSV export, and dark mode.

Deployment

Recommended platforms: Render, Railway, or Heroku.

Make sure Flask app uses the PORT environment variable for deployment:

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


Connect GitHub repo to Render or Railway, set build command:

pip install -r backend/requirements.txt


Start command:

python backend/app.py

Notes

Update the CSV file backend/data/cleaned_covid_data_india.csv as needed.

Keep your virtual environment active when running locally.

For GitHub, you may want a .gitignore to ignore virtual environment and cache files:

venv/
__pycache__/
*.pyc
*.env# covid-data-pipeline
