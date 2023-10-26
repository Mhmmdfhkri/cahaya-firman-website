from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/keranjang")
def keranjang():
    return render_template("keranjang.html")

@app.route("/Checkout")
def Checkout():
    return render_template("Checkout.html")

@app.route("/Payment_Method")
def Payment():
    return render_template("Payment.html")

@app.route("/first")
def fist():
    return render_template("first.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/daftar")
def register():
    return render_template("daftar.html")

@app.route("/products")
def products():
    return render_template("product.html")

@app.route("/contact")
def contact():
    return "<p>Contact Us</p>"

