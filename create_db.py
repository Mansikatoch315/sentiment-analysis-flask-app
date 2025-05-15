from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the SentimentHistory model
class SentimentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to the user
    text = db.Column(db.String(500), nullable=False)  # Text input
    positive = db.Column(db.Float, nullable=False)
    neutral = db.Column(db.Float, nullable=False)
    negative = db.Column(db.Float, nullable=False)
    compound = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<SentimentHistory {self.id}>"

# Create the database and table
with app.app_context():
    db.create_all()

print("Database and tables created!")
