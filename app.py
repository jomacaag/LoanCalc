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
sess = Session()
sess.init_app(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def remove_commas(value):
    if value is not None:
        return value.replace(",", "")
    return value


class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    hash = db.Column(db.String())
    
         

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    username = db.Column(db.String(100))
    loanAmount = db.Column(db.Numeric(scale=2))
    interestRate = db.Column(db.Numeric(scale=2))
    downPayment = db.Column(db.Numeric(scale=2))
    term = db.Column(db.Integer)
    purchasePrice = db.Column(db.Numeric(scale=2))
    loanType = db.Column(db.String(100))
    mortgageInsurance = db.Column(db.Numeric(scale=2))
    upfrontMI = db.Column(db.Numeric(scale=2))
    incomeRate = db.Column(db.String(100))
    monthlyDebt = db.Column(db.Numeric(scale=2))
    propertyTaxes = db.Column(db.Numeric(scale=2))
    CondoHOA = db.Column(db.Numeric(scale=2))
    Hazard = db.Column(db.Numeric(scale=2))
    baseLoanAmount = db.Column(db.Numeric(scale=2))
    income = db.Column(db.Numeric(scale=2))
    MI = db.Column(db.Numeric(scale=2))
    PI = db.Column(db.Numeric(scale=2))
    Interest = db.Column(db.Numeric(scale=2))
    principal = db.Column(db.Numeric(scale=2))
    mipayment = db.Column(db.Numeric(scale=2))
    PITI = db.Column(db.Numeric(scale=2))
    monthlyIncome = db.Column(db.Numeric(scale=2))
    FDTI = db.Column(db.Numeric(scale=2))
    BDTI = db.Column(db.Numeric(scale=2))
    mterm = db.Column(db.Numeric(scale=2))
    LTV = db.Column(db.Numeric(scale=2))

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
    loan_id = request.form.get('loan_id')
    if request.method == 'POST':
        if  loan_id == None:    
            session['purchasePrice'] = purchasePrice = float(remove_commas(request.form.get("purchasePrice")))
            session['interestRate'] = interestRate = float(request.form.get("interestRate"))
            session['downPayment'] = downPayment = float(remove_commas(request.form.get("downPayment")))
            session['loanType'] = loanType = request.form.get("loanType")
            session['mortgageInsurance'] = mortgageInsurance = float(request.form.get("mortgageInsurance"))
            session['upfrontMI'] = upfrontMI = float(request.form.get("upfrontMI"))
            session['term'] = term = float(request.form.get("term"))
            session['income'] = income = float(remove_commas(request.form.get("income")))
            session['incomeRate'] = incomeRate = request.form.get("incomeRate")
            session['monthlyDebt'] = monthlyDebt = float(remove_commas(request.form.get("monthlyDebt")))
            session['propertyTaxes'] = propertyTaxes = float(remove_commas(request.form.get("propertyTaxes")))
            session['CondoHOA'] = CondoHOA = float(remove_commas(request.form.get("CondoHOA")))
            session['Hazard'] = Hazard = float(remove_commas(request.form.get("Hazard")))


            # Calculations:
            session['baseLoanAmount'] =baseLoanAmount = purchasePrice - downPayment
            mterm = 0
            if purchasePrice == 0:
                LTV = 0
            else:
                LTV = ((baseLoanAmount)/purchasePrice)*100
            if loanType == 'Conventional':
                loanAmount = baseLoanAmount
                if LTV <= 0.8:
                    MI = 0
                else:
                    MI = mortgageInsurance/100
            else:
                loanAmount = baseLoanAmount + (baseLoanAmount * (upfrontMI/100))
                if term > 15:
                    if baseLoanAmount <= 726200:
                        if LTV <= 90.00:
                            MI = .0050
                            mterm = 11
                        elif LTV <= 95.00:
                            MI = .0050
                        else:
                            MI = .0055
                    else:
                        if LTV <= 90.00:
                            MI = .007
                            mterm = 11
                        elif LTV <= 95.00:
                            MI = .007
                        else:
                            MI = .0075
                if term <= 15:
                    if baseLoanAmount <= 726200:
                        if LTV <= 90.00:
                            MI = .0015
                            mterm = 11
                        else:
                            MI = .004
                    else:
                        if LTV <= 78.00:
                            MI = .0015
                            mterm = 11
                        elif LTV <= 90.00:
                            MI = .0040
                            mterm = 11
                        else:
                            MI = .0065
                            
            
            session['loanAmount'] = loanAmount               
            session['MI'] = MI
            session['mterm'] = mterm
            session['LTV'] =LTV
            if not interestRate == 0:
                session['PI'] =PI = ((((1000 * interestRate/100) / 12) / (1 - ((12 / (12 + interestRate/100)) ** (term * 12)))) * loanAmount) / 1000
                session['Interest'] =Interest = (loanAmount * interestRate/100 / 12)
                session['principal'] =principal = PI-Interest
            else:
                principal = loanAmount/term/12
                Interest = 0
            
            session['Interest'] = Interest
            session['principal'] = principal 
            session['PI'] = principal + Interest
            session['mipayment'] = mipayment = (baseLoanAmount*MI)/12
            session['PITI'] =PITI =principal+Interest+mipayment+Hazard+CondoHOA+(propertyTaxes)

            if incomeRate == "Hourly":
                monthlyIncome = ((income)*40*52)/12 
            elif incomeRate == "Weekly":
                monthlyIncome = ((income)*52)/12  
            elif incomeRate == "Biweekly":
                monthlyIncome = ((income)*26)/2
            elif incomeRate == "Monthly":
                monthlyIncome = (income)
            elif incomeRate == "Salary":
                monthlyIncome = (income) / 12  
            if not monthlyIncome ==0:
                FDTI = PITI/monthlyIncome*100
                BDTI = (PITI+monthlyDebt)/monthlyIncome*100
            else:
                FDTI=BDTI= 0
            session['monthlyIncome'] =monthlyIncome
            session['FDTI'] = FDTI
            session['BDTI'] = BDTI      
            return render_template('calculated.html', purchasePrice=purchasePrice, interestRate=interestRate,
                                   downPayment=downPayment, loanType=loanType, mortgageInsurance=mortgageInsurance,
                                   upfrontMI=upfrontMI, term=term, income=income, incomeRate=incomeRate,
                                   monthlyDebt=monthlyDebt, propertyTaxes=propertyTaxes, CondoHOA=CondoHOA,
                                   Hazard=Hazard, loanAmount=loanAmount, PITI=PITI, FDTI=FDTI, BDTI=BDTI, LTV=LTV, 
                                   PI=principal+Interest, Interest=Interest, MI=MI, mipayment=mipayment, 
                                   principal=principal, baseLoanAmount=baseLoanAmount,mterm=mterm )
        else:
            loan = Loan.query.get(loan_id)
            return render_template('calculated.html', purchasePrice=loan.purchasePrice, interestRate=loan.interestRate,
                                   downPayment=loan.downPayment, loanType=loan.loanType, mortgageInsurance=loan.mortgageInsurance,
                                   upfrontMI=loan.upfrontMI, term=loan.term, income=loan.income, incomeRate=loan.incomeRate,
                                   monthlyDebt=loan.monthlyDebt, propertyTaxes=loan.propertyTaxes, CondoHOA=loan.CondoHOA,
                                   Hazard=loan.Hazard, loanAmount=loan.loanAmount, PITI=loan.PITI, FDTI=loan.FDTI, BDTI=loan.BDTI, LTV=loan.LTV, 
                                   PI=loan.principal+loan.Interest, Interest=loan.Interest, MI=loan.MI, mipayment=loan.mipayment, 
                                   principal=loan.principal, baseLoanAmount=loan.baseLoanAmount,mterm=loan.mterm )
    return redirect('/')

@app.route('/history', methods=["GET", "POST"])
@login_required
def history():
    user = users.query.get(session.get("user_id"))
    if user is None:
        flash('You must be logged in to do that.!')
        return redirect('/login')
    else:
        if request.method == 'POST':
            # Access the values from the session
            purchasePrice = session.get('purchasePrice')
            interestRate = session.get('interestRate')
            downPayment = session.get('downPayment')
            loanType = session.get('loanType')
            mortgageInsurance = session.get('mortgageInsurance')
            upfrontMI = session.get('upfrontMI')
            term = session.get('term')
            income = session.get('income')
            incomeRate = session.get('incomeRate')
            monthlyDebt = session.get('monthlyDebt')
            propertyTaxes = session.get('propertyTaxes')
            CondoHOA = session.get('CondoHOA')
            Hazard = session.get('Hazard')
            baseLoanAmount = session.get('baseLoanAmount')
            MI = session.get('MI')
            PI = session.get('PI')
            Interest = session.get('Interest')
            principal = session.get('principal')
            mipayment = session.get('mipayment')
            PITI = session.get('PITI')
            monthlyIncome = session.get('monthlyIncome')
            FDTI = session.get('FDTI')
            BDTI = session.get('BDTI')
            LTV = session.get('LTV')
            loanAmount = session.get('loanAmount')
            mterm = session.get('mterm')
            
            
            existing_loan = Loan.query.filter_by(username=user.username,
                    purchasePrice=purchasePrice,interestRate=interestRate,downPayment=downPayment,
                    loanType=loanType,mortgageInsurance=mortgageInsurance,upfrontMI=upfrontMI,term=term,
                    income=income,incomeRate=incomeRate,monthlyDebt=monthlyDebt,propertyTaxes=propertyTaxes,
                    CondoHOA=CondoHOA,Hazard=Hazard,baseLoanAmount=baseLoanAmount,MI=MI,PI=PI,Interest=Interest,
                    principal=principal,mipayment=mipayment,PITI=PITI,monthlyIncome=monthlyIncome,
                    FDTI=FDTI,BDTI=BDTI,LTV=LTV,loanAmount=loanAmount, mterm=mterm).first()
            if existing_loan:
                loan_id = existing_loan.id  # Retrieve the ID of the existing loan
                flash("Loan with the same scenario already exists")
                flash("Loan ID: "+ str(loan_id))
            else:
                loan = Loan(
                    username=user.username, purchasePrice=purchasePrice,
                    interestRate=interestRate, downPayment=downPayment,
                    loanType=loanType, mortgageInsurance=mortgageInsurance,
                    upfrontMI=upfrontMI, term=term,
                    income=income, incomeRate=incomeRate,
                    monthlyDebt=monthlyDebt, propertyTaxes=propertyTaxes, CondoHOA=CondoHOA, Hazard=Hazard,
                    baseLoanAmount=baseLoanAmount,
                    MI=MI, PI=PI,  Interest=Interest,  principal=principal,  mipayment=mipayment,
                    PITI=PITI, monthlyIncome=monthlyIncome, FDTI=FDTI, BDTI=BDTI, LTV=LTV, loanAmount=loanAmount,
                    mterm=mterm
                )
                db.session.add(loan)
                db.session.commit()
                loan_id = loan.id
                flash("Loan Scenario : " + str(loan_id) + " Saved Successfully")
                
            Loans  = Loan.query.filter_by(username=user.username).all()
            return render_template('history.html', Loans = Loans)
        Loans  = Loan.query.filter_by(username=user.username).all()
        return render_template('history.html', Loans = Loans)

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

    
    

if __name__ == "__main__": app.run()
# if __name__ == "__main__": app.run