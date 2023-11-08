from main import db

class Order_detail(db.Model):
    __tablename__ = 'order_detail'
    id_order = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    order_status = db.Column(db.String(100)) 
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user')) 
    id_payment = db.Column(db.Integer, db.ForeignKey('payment_detail.id_payment')) 
    

    user = db.relationship('User', backref='Order_detail')  # Hubungan dengan objek Users
    payment_detail = db.relationship('Payment_detail', backref='Order_detail', foreign_keys=[id_payment])  
