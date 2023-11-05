from main import app, db, bcrypt, login_manager
from flask import render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from forms.auth_forms import RegisterForm, LoginForm
from flask_login import login_user,login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask import flash
from models.user import User
from models.product import Barang



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("first.html")


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
@login_required
def Checkout():
    return render_template("checkout.html",user=current_user)


@app.route("/payment")
def Payment():
    return render_template("Payment.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                print("User logged in successfully")
                return redirect(url_for('home'))
        print("Invalid login credentials")
    return render_template("login.html", form=form)


@app.route("/daftar", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("daftar.html", form=form)


@app.route("/products")
def products():
    return render_template("product.html")

# admin start
@app.route("/admin_user")
def admin_user():
    users = User.query.all()
    return render_template("admin_user.html", users=users)

@app.route("/admin_crud")
def admin_crud():
    barang_list = Barang.query.all()
    return render_template('admin_crud.html', barang_list=barang_list)


@app.route("/admin_status")
def admin_status():
    return render_template("admin_status.html")
# admin end

# crud

@app.route("/add")
def add():
    return render_template("add.html")

@app.route('/add_barang', methods=['POST'])
def add_barang():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        category = request.form['category']
        quantityInStock = request.form['quantityInStock']
        price = request.form['price']

        # Check if a file is uploaded
        if 'picture' in request.files:
            picture = request.files['picture']
            if picture.filename != '':
                # Save the file to the "uploads" directory
                picture_filename = secure_filename(picture.filename)
                picture.save('static/unggah/' + picture_filename)
            else:
                picture_filename = None
        else:
            picture_filename = None

        # Create a new Barang object and save it to the database
        new_barang = Barang(name=name, desc=desc, category=category, quantityInStock=quantityInStock, price=price, picture=picture_filename)
        db.session.add(new_barang)
        db.session.commit()
        return redirect(url_for("add"))

    return render_template("add.html")





@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_barang(id):
    barang = Barang.query.get_or_404(id)
    if request.method == 'POST':
        # Update the 'Barang' item with the new data
        barang.name = request.form['name']
        barang.desc = request.form['desc']
        barang.category = request.form['category']
        barang.quantityInStock = request.form['quantityInStock']
        barang.price = request.form['price']

         # Check if a file is uploaded
        if 'picture' in request.files:
            picture = request.files['picture']
            if picture.filename != '':
                # Save the file to the "uploads" directory
                picture_filename = secure_filename(picture.filename)
                picture.save('static/unggah/' + picture_filename)
            else:
                picture_filename = None
        else:
            picture_filename = None

        db.session.commit()
        flash('Barang updated successfully', 'success')
        return redirect(url_for('admin_crud'))
    return render_template("edit.html", barang=barang)

@app.route("/delete/<int:id>", methods=['POST'])
def delete_barang(id):
    barang = Barang.query.get_or_404(id)
    db.session.delete(barang)
    db.session.commit()
    flash('Barang deleted successfully', 'success')
    return redirect(url_for('admin_crud'))


@app.route("/contact")
def contact():
    return "<p>Contact Us</p>"

@app.route("/profil")
@login_required
def profil():
    return render_template("profil.html",user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

