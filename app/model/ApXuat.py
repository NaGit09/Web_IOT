from app import db
from datetime import datetime

class ApXuat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ApXuat = db.Column(db.Float)
    TrangThai = db.Column(db.String(50))
    DienAp = db.Column(db.Float)
    ThoiGian = db.Column(db.DateTime, default=datetime.utcnow)
