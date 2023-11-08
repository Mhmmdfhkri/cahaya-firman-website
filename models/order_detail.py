from main import db

class Order_detail(db.Model):
    __tablename__ = 'order_detail'
    id_order = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    order_status = db.Column(db.VARCHAR(100)) 
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))  # foreign key ke tabel "users"
    id_payment = db.Column(db.Integer, db.ForeignKey('payment_detail.id_payment'))  # foreign key ke tabel "payment_detail"
    
    # Menambahkan hubungan dengan objek Users dan Payment_detail untuk mengakses data terkait.
    user = db.relationship('user', backref='order_detail')  # Hubungan dengan objek Users
    payment_detail = db.relationship('payment_detail', backref='order_detail')  # Hubungan dengan objek Payment_detail
