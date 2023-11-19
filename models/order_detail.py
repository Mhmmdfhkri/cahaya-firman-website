from main import db

class Order_detail(db.Model):
    __tablename__ = 'order_detail'
    id_order = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    order_status = db.Column(db.String(100)) 
    id_payment = db.Column(db.Integer, db.ForeignKey('payment_detail.id_payment', name='fk_oDetail_payment'))
    id_session = db.Column(db.Integer, db.ForeignKey('session.id_session', name='fk_oDetail_session'))

    payment_detail = db.relationship('Payment_detail', back_populates='order_detail')
    session = db.relationship('session', back_populates='Order_detail')