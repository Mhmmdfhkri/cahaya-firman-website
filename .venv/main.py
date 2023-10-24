from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, World!</p>"


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

@app.route("/contact")
def contact():
    return "<p>Contact Us</p>"
