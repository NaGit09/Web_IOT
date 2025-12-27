from app import db
from datetime import datetime

class INVTG20(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TanSo = db.Column(db.Integer)
    DongDien = db.Column(db.Float)
    ThoiGian = db.Column(db.DateTime, default=datetime.utcnow)