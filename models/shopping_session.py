from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class session(db.Model):
    id_session = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=True)
    total = db.Column(db.Float, nullable=False, unique=False)

    user = relationship("User", backref="session")  

