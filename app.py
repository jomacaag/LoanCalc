import os
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "loancalc.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


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

    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)