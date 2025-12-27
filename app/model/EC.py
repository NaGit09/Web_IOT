from app import db
from datetime import datetime

class ED(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Raw = db.Column(db.Integer)
    Voltage = db.Column(db.Float)
    EC = db.Column(db.Float)
    ThoiGian = db.Column(db.DateTime, default=datetime.utcnow)