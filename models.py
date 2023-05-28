from .app import db 
from datetime import datetime

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    affiliation = db.Column(db.String)
    comment = db.Column(db.String)