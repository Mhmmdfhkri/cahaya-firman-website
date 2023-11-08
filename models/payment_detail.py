from main import db

class Payment_detail(db.Model):
    __tablename__ = 'payment_detail'  
    id_payment = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer(100)) 
    payment_method = db.Column(db.Varchar(100)) 
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'))  # Foreign key ke tabel Orders
    
    
    order = db.relationship('order_detail', backref='payment_detail')  # Hubungan dengan objek Orders
