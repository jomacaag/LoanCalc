import os
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, session
from flask_session import Session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from functools import wraps
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text


# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "loancalc.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    hash = db.Column(db.String())
    
         

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    loan_amount = db.Column(db.Numeric(scale=2))
    interest_rate = db.Column(db.Numeric(scale=2))
    income = db.Column(db.Numeric(scale=2))
    income_rate = db.Column(db.String(100))
    debts = db.Column(db.Numeric(scale=2))
    down_payment = db.Column(db.Numeric(scale=2))
    loan_type = db.Column(db.String(100))
    mi = db.Column(db.Numeric(scale=2))
    Upfront_Mi = db.Column(db.Numeric(scale=2))
    taxes = db.Column(db.Numeric(scale=2))
    condo_fee_hoa = db.Column(db.Numeric(scale=2))
    insurance = db.Column(db.Numeric(scale=2))
    term = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Loan(id={self.id}, loan_amount={self.loan_amount}, loan_type={self.loan_type})"


@app.cli.command("initdb")
def reset_db():
    """Drops and Creates fresh database"""
    with app.app_context():
        db.drop_all()
        db.create_all()

    print("Initialized default DB")


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash('You must be logged in to do that.')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculated', methods=['GET', 'POST'])
def calculated():
    if request.method == 'POST':
        
        return render_template('calculated.html')
    return redirect('/')

@app.route('/history')
@login_required
def history():
    user = users.query.get(session["user_id"])
    return render_template('history.html', username=user.username)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return flash("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return flash("must provide password")

        # Query database for username
        rows = db.session.execute(text("SELECT * FROM users WHERE username = :username"), {"username": request.form.get("username")})
        user = rows.fetchone()
        
        if user is None or not check_password_hash(user.hash, request.form.get("password")):
            # Invalid login credentials
            flash("Invalid username or password")
            return redirect('/login')

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page\
        flash('Login successful')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return redirect("/register")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect("/register")
        elif not request.form.get("confirmation"):
            flash("must confirm password")
            return redirect("/register")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmpass = request.form.get("confirmation")
        
        checkuser = db.session.execute(text("SELECT username FROM users WHERE username = :username"), {"username": username}).fetchone()
        if checkuser is not None:
            flash("Username is taken")
            return redirect("/register")
        
        # Additional password validation can be added here
        
        if password == confirmpass:
            passhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            try:
                db.session.execute(text("INSERT INTO users (username, hash) VALUES (:username, :passhash)"), {"username": username, "passhash": passhash})
                db.session.commit()
                user = users.query.filter_by(username=username).first()
                session["user_id"] = user.id 
                flash("Registration Successful")
                return redirect("/")
            except IntegrityError:
                db.session.rollback()
                flash("An error occurred while registering")
                return redirect("/register")
        else:
            flash("Passwords do not match")
            return redirect("/register")
    else:
        return render_template("register.html")
    
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

    
    



if __name__ == "__main__":
    app.run(debug=True)