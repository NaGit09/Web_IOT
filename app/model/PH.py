from app import db
from datetime import datetime

class PH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Raw = db.Column(db.Integer)
    Voltage = db.Column(db.Float)
    PH = db.Column(db.Float)
    ThoiGian = db.Column(db.DateTime, default=datetime.utcnow)