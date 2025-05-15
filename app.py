from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from werkzeug.security import generate_password_hash, check_password_hash
import nltk
from nltk.corpus import stopwords
from flask_mail import Mail, Message
from flask import flash, redirect, url_for

# Download stopwords
nltk.download('stopwords')

# Flask app initialization
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password'     # use App Password or secure method
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)
app.secret_key = 'replace_with_your_real_secret_key'  # Replace this securely

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Sentiment history model
class SentimentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    positive = db.Column(db.Float)
    neutral = db.Column(db.Float)
    negative = db.Column(db.Float)
    compound = db.Column(db.Float)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # your form processing and sending email code here
        
        # After successful send:
        flash('Message sent successfully!', 'success')  # 'success' category makes green alert
        return redirect(url_for('contact'))

    return render_template('contact.html')



@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('sentiment'))
    return redirect(url_for('login'))


@app.route('/sentiment', methods=['GET'])
@login_required
def sentiment():
    return render_template('form.html', title="Sentiment Analysis")

@app.route('/sentiment', methods=['POST'])
@login_required
def analyze_sentiment():
    stop_words = set(stopwords.words('english'))
    text1 = request.form['text1'].lower()
    text_final = ''.join(c for c in text1 if not c.isdigit())
    processed = ' '.join([word for word in text_final.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    scores = sa.polarity_scores(processed)
    compound = round((1 + scores['compound']) / 2, 2)

    record = SentimentRecord(
        user_id=current_user.id,
        text=text_final,
        positive=scores['pos'],
        neutral=scores['neu'],
        negative=scores['neg'],
        compound=compound
    )
    db.session.add(record)
    db.session.commit()

    return render_template('form.html', final=compound, text1=text_final,
                           text2=scores['pos'], text3=scores['neu'],
                           text4=compound, text5=scores['neg'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        user = User(username=username, password_hash=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('User successfully logged in!', 'success')
            return render_template('login.html', redirect_after_login=True)  # Don't redirect yet
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    records = SentimentRecord.query.filter_by(user_id=current_user.id).all()

    if records:
        positive_avg = sum(record.positive for record in records) / len(records)
        neutral_avg = sum(record.neutral for record in records) / len(records)
        negative_avg = sum(record.negative for record in records) / len(records)
    else:
        positive_avg = neutral_avg = negative_avg = 0

    labels = [f'Entry {i+1}' for i in range(len(records))]
    positive = [record.positive for record in records]
    neutral = [record.neutral for record in records]
    negative = [record.negative for record in records]

    return render_template('dashboard.html', records=records,
                           labels=labels, positive=positive,
                           neutral=neutral, negative=negative,
                           average_positive=positive_avg,
                           average_neutral=neutral_avg,
                           average_negative=negative_avg)

@app.route('/delete_all_history', methods=['POST'])
@login_required
def delete_all_history():
    SentimentRecord.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Your sentiment history has been deleted.', 'success')
    return redirect(url_for('dashboard'))

# Main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
