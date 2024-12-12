from flask import Flask, render_template, request, session, redirect,flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import requests
from functools import wraps
from flask_login import LoginManager, login_required, UserMixin, logout_user, current_user, login_user
import time

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)
login_manager.init_app(app)
db = SQLAlchemy(app)


def get_token():
    url = "https://ebankily-tst.appspot.com/authentification"
    body ={
        "grant_type" : "password",
        "username" : "IMTIYAZ",
        "password" : "12345",
        "client_id" : "ebankily",
    }
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
   
    response = requests.post(url, data=body, headers=headers)
    token = response.json().get('access_token')
    return token
access_token = ''

def bankily_payment(data):
    url = "https://ebankily-tst.appspot.com/payment"
    access_token = get_token()
    headers = {
        "Authorization" :  f"Bearer {access_token}",
        "Content-type" : "application/json"
    }
    body = {
        "clientPhone": data.get("clientPhone"),
        "passcode": data.get("passcode"),
        "operationId": data.get("operationId"),
        "amount": data.get("amount"),
        "language": data.get("language"),
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()

def bankily_check_transaction(operationID):
    url = "https://ebankily-tst.appspot.com/checkTransaction"
    headers = {
        "Authorization" :  f"Bearer {access_token}",
        "Content-type" : "application/json"
    }

    body={
        "operationID":operationID
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    balance = db.Column(db.Float, default=0)
    operations = db.relationship('BankilyOperation', backref='user')
    create_date = db.Column(db.Date, default=datetime.now)

class BankilyOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    operationid = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.Date, default=datetime.now)

# Définir la fonction user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Récupère l'utilisateur à partir de l'ID

@app.route('/payment',  methods=['POST','GET'])  # Ajout du décorateur
@login_required
def payment():
    operationId = str(int(time.time()))
    if request.method == 'POST':
        response = bankily_payment({
            "clientPhone": request.form.get('clientPhone'),
            "passcode": request.form.get('passcode'),
            "operationId": operationId,
            "amount": request.form.get('amount'),
            "language": request.form.get('language'),
        })
        if response.get('errorCode') == 0:
            response = bankily_check_transaction(operationId)
            if response.get('errorCode') == 0:
                current_user.balance += float(request.form.get('amount'))
                db.session.commit()
                flash(f'Paiement réuissi !', 'success')
                return render_template('confirmation.html')
            else:
                flash(f'Erreur lors de la vérification du paiement{response}','danger')
                return render_template('errors.html')
        else:
            flash(f'Erreur lors de la l\'opération de paiement{response}', 'danger')
            return render_template('errors.html')

    return render_template('payment.html')

@app.route('/')  # Ajout du décorateur
def index():
    if current_user.is_authenticated:
        return redirect(url_for('payment'))
    return render_template('index.html')

@app.route('/logout')  # Ajout du décorateur
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/confirmation')  # Ajout du décorateur
def confirmation():
    return render_template('confirmation.html')

@app.route('/login', methods=['POST','GET'])  # Ajout du décorateur
def login():
    user_email = request.form.get('loginEmail')
    user_password = request.form.get('loginPassword')
    user = User.query.filter_by(email=user_email).first()
    if user:
        userBytes = user_password.encode('utf-8')
        result = bcrypt.checkpw(userBytes, user.password)
        if result:
            login_user(user)
            return redirect(url_for('payment'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
            return redirect(url_for('index'))
    else:
        flash('Email ou mot de passe incorrect', 'danger')
        return redirect(url_for('index'))


@app.route('/register', methods=['POST'])  # Ajout du décorateur
def register():
    user_name = request.form.get('signupName')
    user_email = request.form.get('signupEmail')
    user_password = request.form.get('signupPassword')
    user = User()
    user.name = user_name
    user.email = user_email

    bytes = user_password.encode('utf-8')
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt) 
    user.password =hash
    db.session.add(user)
    db.session.commit()
    session['name'] = user.name
    session['email'] = user.email
    session['balance'] = user.balance
    return redirect(url_for('payment'))

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True, host="0.0.0.0")