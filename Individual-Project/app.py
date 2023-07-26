from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
# DataBase Configuration
config = {
  "apiKey": "AIzaSyCPtYaQIBk8M-Cm4zMWy87G8bv4DeG_Dkg",
  "authDomain": "personal-proj-countries.firebaseapp.com",
  "projectId": "personal-proj-countries",
  "storageBucket": "personal-proj-countries.appspot.com",
  "messagingSenderId": "863082590393",
  "appId": "1:863082590393:web:4e431cdb7c091cc5262b68",
  "measurementId": "G-G3Y6SB1Z0K",
  "databaseURL": "https://personal-proj-countries-default-rtdb.firebaseio.com/"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        country = request.form['country']
        try:
            login_session["user"] = auth.create_user_with_email_and_password(email, password)
            UID = login_session["user"]["localId"]
            user = {"username": username, "email": email, "country": country}
            db.child("users").child(UID).set(user)
            return redirect(url_for("viewcountry", country = country))
        except:
            error = "Sign Up fError"
    return render_template("signup.html")

@app.route("/signin", methods = ['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session["user"] = auth.sign_in_with_email_and_password(email, password)
            UID = login_session["user"]["localId"]
            country = db.child("users").child(UID).get().val()["country"]
            return redirect(url_for("viewcountry", country = country))
        except:
            error = "signin failed"
    return render_template("signin.html")

@app.route("/signout", methods = ['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for("signin"))

@app.route("/country/<string:country>", methods = ['GET', 'POST'])
def viewcountry(country):
    if request.method == "POST":
        destination = request.form['destination']
        db.child("Countries").child(country).child("tourism").push(destination)
    else:
        try:
            UID = login_session["user"]["localId"]
            user_logged = db.child("users").child(UID).get().val()
            assert user_logged != None
        except:
            return redirect(url_for("signin"))
    UID = login_session["user"]["localId"]
    user_logged = db.child("users").child(UID).get().val()
    countries = db.child("Countries").get().val()
    country_logged = db.child("Countries").child(country).get().val()
    return render_template("country.html", country = country, countries = countries, country_logged = country_logged, user_logged = user_logged)

if __name__ == '__main__':
    app.run(debug=True)