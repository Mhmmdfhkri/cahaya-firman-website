from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class session(db.Model):
    id_session = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    total = db.Column(db.Float, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    orders = db.relationship('Order_items', backref='order_session', lazy=True)

    user = relationship("User", backref="session")  

