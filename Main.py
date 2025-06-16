import datetime
import os

from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from functions import Functions

# Master
app = Flask(__name__)
app.secret_key = "Peter"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
functions = Functions()

# Routes
@app.route("/", methods = ["GET", "POST"])
def index():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        if request.form.get("event") == "add-entry":
            mileage = request.form.get("mileage")
            date = request.form.get("date")
            description = request.form.get("description")
            price = request.form.get("price")
            new_entry = DbData(mileage = mileage, date = date, description = description, price = price)
            db.session.add(new_entry)
            db.session.commit()

    entries = DbData.query.order_by(DbData.mileage).all()
    return render_template("index.html", today = today, entries = entries)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        session.update({"name":name}) # The preferred version : session["name"] = name
        return redirect("/user")

    return render_template("login.html")

@app.route("/user", methods = ["GET", "POST"])
def user():
    if "name" in session:
        name = session.get("name")
        return render_template("user.html", name = name)

    return redirect("/login")

# Db model
class DbData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)  # NULL in SQL
    mileage = db.Column(db.Integer)
    price = db.Column(db.Float)
    date = db.Column(db.String(20))

    def __repr__(self) -> str:
        return f"Entry : {self.id}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug = True)