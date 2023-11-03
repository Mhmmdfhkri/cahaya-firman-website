from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:\data\db'  # Menggunakan SQLite sebagai database sederhana
db = SQLAlchemy(app)

class Barang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    category = db.Column(db.String(100))
    quantityInStock = db.Column(db.Integer)
    price = db.Column(db.Float)
    picture = db.Column(db.String(100))

db.create_all()

