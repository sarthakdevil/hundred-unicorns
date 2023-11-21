from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="static/")

DB_NAME = "database.db"
app.config['SECRET_KEY'] = "1234"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), unique=True)
    name = db.Column(db.String(300))
    password = db.Column(db.String(150))
    posts = db.relationship("Post")

with app.app_context():
    if not path.exists(DB_NAME):
        db.create_all()


# ROUTES

@app.route("/")
def home():
        return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("passwd")
        
        print(f"email = {email}, passwd = {password}")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("logged in")
                return redirect(url_for("home"), code=302)

            else:
                flash("incorrect password")
        else:
            flash("you need to signup first")
        
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("passwd1")
        password2 = request.form.get("passwd2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("email already in use")
        

        elif password1 != password2:
            flash("Re-Enter the same password")

        else:

            new_user = User(name=name, email=email, password=generate_password_hash(password1))
            print(f"name = {name}, email = {email}, passwd = {password1}")
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/dump-users")
def dump():
    users = User.query.order_by(User.id)
    return " ".join(user.name for user in users)

@app.route("/forums", methods=['GET', 'POST'])
def forum():
    if request.method == "POST":
        return "Huge L on you, haven't implimented it yet LOL"
    return render_template("forum.html")

if __name__ == "__main__":
    app.run(debug=True)
