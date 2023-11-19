from main import db
from datetime import datetime

class Payment_detail(db.Model):
    __tablename__ = 'payment_detail'  
    id_payment = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer) 
    payment_method = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow) 

    order_detail = db.relationship('Order_detail', back_populates='payment_detail')
