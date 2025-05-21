Sentiment Analysis Web App using Flask & VADER

This is a web application that performs sentiment analysis on user-input text using the VADER model from NLTK. It allows users to register, log in, analyze the sentiment of text (positive, neutral, or negative), view their sentiment analysis history, and visualize the results on a dashboard.

📌 Project Explanation

The app is built with Python and Flask on the backend and HTML/CSS for the frontend. It leverages the VADER (Valence Aware Dictionary and sEntiment Reasoner) model for sentiment classification. The application is suitable for understanding user opinions, customer feedback, and emotional trends in texts.


✨ Features

User Registration & Login System

Sentiment Analysis (Positive, Negative, Neutral)

History of Sentiment Analyses per User

Dashboard Visualization with Graphs

Contact Form with Email Functionality

Responsive UI using Bootstrap


⚙️ Requirements

Before running the project, make sure these tools are installed on your system:

1. Python (3.8 or above)

2. pip (Python package manager)

3. Git (to clone the project from GitHub)



📥 Installation & Setup (Step-by-Step)

Follow these steps to set up and run the project on any computer (e.g., in college lab):

1. Clone the Project

Open Terminal or Command Prompt:

git clone https://github.com/Mansikatoch315/sentiment-analysis-flask-app.git
cd sentiment-analysis-flask-app

2. Create and Activate a Virtual Environment (optional but recommended)

python -m venv venv

Activate it:   Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate


3. Install Required Python Libraries

pip install -r requirements.txt

This will install all necessary libraries like Flask, SQLAlchemy, flask-login, flask-mail, nltk, etc.

4. Download NLTK Data (Only Once)

In Python shell:

import nltk
nltk.download('stopwords')

5. Run the Application

python app.py

Then open your browser and go to:

http://127.0.0.1:5002



📤 If Running on a New Computer

Make sure to install:

Python

pip

Git


Then follow steps 1 to 5 above.

If not using a virtual environment, make sure all packages are installed globally using:

pip install flask flask-login flask-mail flask-sqlalchemy nltk vaderSentiment


✉️ Email Configuration (For Contact Form)

In app.py, update these lines with your own email and app password:

app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

For Gmail, make sure "Less secure apps" is allowed or use App Password.


🗃️ Folder Structure

sentiment-analysis-flask-app/
│
├── app.py
├── requirements.txt
├── sentiments.db
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
├── static/
│   └── style.css
└── README.md


---

🧪 Sample Test Credentials

You can register a new user or modify the SQLite database directly for quick access.


---

📈 Libraries Used

Flask

Flask-Login

Flask-Mail

Flask-SQLAlchemy

NLTK (VADER & Stopwords)

Chart.js

Bootstrap 4




