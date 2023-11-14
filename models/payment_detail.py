from main import db

class Payment_detail(db.Model):
    __tablename__ = 'payment_detail'  
    id_payment = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer) 
    payment_method = db.Column(db.String(100)) 
