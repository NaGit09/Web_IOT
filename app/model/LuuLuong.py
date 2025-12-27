from app import db
from datetime import datetime

class LuuLuong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LuuLuongID = db.Column(db.Integer)
    SoXung = db.Column(db.Integer)
    LP = db.Column(db.Float)
    LS = db.Column(db.Float)
    TongLuuLuong = db.Column(db.Float)
    ThoiGian = db.Column(db.DateTime, default=datetime.utcnow)