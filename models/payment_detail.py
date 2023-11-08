from main import db

class Payment_detail(db.Model):
    __tablename__ = 'payment_detail'  
    id_payment = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer) 
    payment_method = db.Column(db.String(100)) 
    id_order = db.Column(db.Integer, db.ForeignKey('order_detail.id_order'))  
    
    
    order = db.relationship('Order_detail', backref='Payment_detail', foreign_keys=[id_order]) 
