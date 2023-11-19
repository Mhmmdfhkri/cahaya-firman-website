from main import app, db, bcrypt, login_manager
from flask import render_template, url_for, redirect, request, flash,session as flask_session,g
from werkzeug.utils import secure_filename
from forms.auth_forms import RegisterForm, LoginForm
from flask_login import login_user,login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask import flash
from models.user import User
from models.product import Product
from models.order_detail import Order_detail
from models.order_items import Order_items
from models.payment_detail import Payment_detail
from models.reviews import reviews
from models.shopping_session import session
from sqlalchemy.orm.collections import InstrumentedList
from datetime import datetime


# Define the reduce_quantity_in_stock function
def reduce_quantity_in_stock(product_id, quantity):
    # Get the product based on product_id
    product = Product.query.get_or_404(product_id)

    # Check if there is enough quantity in stock
    if product.quantityInStock >= quantity:
        # Reduce the quantityInStock
        product.quantityInStock -= quantity

        # Commit the changes to the database
        db.session.commit()

        return True
    else:
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def products():
    barang_list = Product.query.all()
    return render_template("product.html", barang_list=barang_list,user = current_user)




def get_product(id_product):
    return Product.query.get(id_product)


# Rute untuk menampilkan halaman detail produk berdasarkan ID produk
@app.route('/detail_product/<int:id_product>')
def detail_product(id_product):
    # Dapatkan detail produk dan ulasan berdasarkan product_id
    product = get_product(id_product)
    return render_template('detail_product.html', product=product)

@app.route("/home")
def home():
    return render_template("home.html",user = current_user)


@app.route("/about")
def about():
    return render_template("about.html",user = current_user)


@app.route("/keranjang")
def keranjang():
    # Check if the user has an active session
    active_session = None
    if current_user.session:
        for session in current_user.session:
            if session.is_active:
                active_session = session
                break

    # If there is an active session, get the order items
    order_items = []
    if active_session:
        order_items = Order_items.query.filter_by(id_session=active_session.id_session).all()

    # Calculate total price
    total_price = sum(order_item.quantity * order_item.product.price for order_item in order_items)

    return render_template("keranjang.html", order_items=order_items, user=current_user, total_price=total_price)


@app.route("/Checkout", methods=["GET", "POST"])
@login_required
def Checkout():
    # Check if the user has an active session
    if current_user.session is None or not any(sess.is_active for sess in current_user.session):
        new_session = session(id_user=current_user.id_user, total=0)
        db.session.add(new_session)
        db.session.commit()

    # Find the active session in the list
    active_session = next(sess for sess in current_user.session if sess.is_active)

    if active_session:
        order_items = Order_items.query.filter_by(id_session=active_session.id_session).all()
        total_price = sum(order_item.quantity * order_item.product.price for order_item in order_items)
        return render_template("Checkout.html", user=current_user, order_items=order_items, total_price=total_price)

    flash("No active session to checkout", "danger")
    return redirect(url_for("keranjang"))


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


# admin start
@app.route("/admin_user")
def admin_user():
    users = User.query.all()
    return render_template("admin_user.html", users=users)

@app.route("/admin_crud")
def admin_crud():
    barang_list = Product.query.all()
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
        new_barang = Product(name=name, desc=desc, category=category, quantityInStock=quantityInStock, price=price, picture=picture_filename)
        db.session.add(new_barang)
        db.session.commit()
        return redirect(url_for("admin_crud"))

    return render_template("add.html")



@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_barang(id):
    barang = Product.query.get_or_404(id)
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
    barang = Product.query.get_or_404(id)
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

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        user = current_user

        # Update user data based on form input
        user.fullname = request.form.get('fullname')
        user.telephone = request.form.get('telephone')
        user.email = request.form.get('email')
        user.gender = request.form.get('gender')
        user.address = request.form.get('address')

        db.session.commit()
        flash('Profile updated successfully', 'success')

    return redirect(url_for('profil'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_to_cart/<int:id_product>', methods=['POST'])
@login_required
def add_to_cart(id_product):
    # Get the product based on id_product
    product = Product.query.get_or_404(id_product)

    # Check if the user has an active session
    if current_user.session is None or not any(sess.is_active for sess in current_user.session):
        new_session = session(id_user=current_user.id_user, total=0)
        db.session.add(new_session)
        db.session.commit()

    # Find the active session in the list
    active_session = next(sess for sess in current_user.session if sess.is_active)

    # Check if the product is already in the cart
    existing_order_item = Order_items.query.filter_by(id_product=id_product, id_session=active_session.id_session).first()

    # Define new_order_item outside the if block
    new_order_item = None

    if existing_order_item:
        # If the item is already in the cart, increase the quantity
        existing_order_item.quantity += 1
    else:
        # If the item is not in the cart, create a new order item
        new_order_item = Order_items(id_product=id_product, id_session=active_session.id_session, quantity=1)
        db.session.add(new_order_item)

    # Commit the changes to the database
    db.session.commit()

    # Store the order items in flask.g only if new_order_item is defined
    if new_order_item:
        g.setdefault('order_items', []).append(new_order_item)

    flash(f'{product.name} added to the cart', 'success')
    return redirect(url_for('keranjang'))

@app.route('/update_cart/<int:id_order_item>', methods=['POST'])
@login_required
def update_cart(id_order_item):
    # Get the order item based on id_order_item
    order_item = Order_items.query.get_or_404(id_order_item)

    # Update the quantity or remove the item based on the form submission
    if 'plus' in request.form:
        order_item.quantity += 1
    elif 'minus' in request.form:
        if order_item.quantity > 1:
            order_item.quantity -= 1
        else:
            # If the quantity is 1, consider removing the item from the cart
            db.session.delete(order_item)

    # Commit the changes to the database
    db.session.commit()

    # Redirect back to the cart page
    flash('Cart updated successfully', 'success')
    return redirect(url_for('keranjang'))

@app.route('/update_checkout/<int:id_order_item>', methods=['POST'])
@login_required
def update_checkout(id_order_item):
    # Get the order item based on id_order_item
    order_item = Order_items.query.get_or_404(id_order_item)

    # Update the quantity or remove the item based on the form submission
    if 'plus' in request.form:
        order_item.quantity += 1
    elif 'minus' in request.form:
        if order_item.quantity > 1:
            order_item.quantity -= 1
        else:
            # If the quantity is 1, consider removing the item from the cart
            db.session.delete(order_item)

    # Commit the changes to the database
    db.session.commit()

    # Redirect back to the cart page
    flash('item updated successfully', 'success')
    return redirect(url_for('Checkout'))


@app.route('/checkout_bt', methods=['POST'])
@login_required
def checkoutbt():
    # Check if the user has an active session
    active_session = None
    if current_user.session:
        for sess in current_user.session:
            if sess.is_active:
                active_session = sess
                break

    if active_session:
        # Calculate total price
        order_items = Order_items.query.filter_by(id_session=active_session.id_session).all()
        total_price = sum(order_item.quantity * order_item.product.price for order_item in order_items)

        # Check if there are order items to proceed
        if order_items:
            # Create a new payment_detail object
            new_payment = Payment_detail(amount=total_price, payment_method='Your Payment Method', payment_date=datetime.utcnow())
            db.session.add(new_payment)
            db.session.commit()

            # Create a new order_detail object
            new_order = Order_detail(total=total_price, order_status='Pending', id_payment=new_payment.id_payment, id_session=active_session.id_session)

            new_order.order_items = []

            # Link the order_detail to the order_items
            for order_item in order_items:
                print(f'Appending order_item with id {order_item.id_order_item} to new_order.order_items')
                new_order.order_items.append(order_item)

                # Reduce the quantityInStock
                product_id = order_item.product.id_product
                quantity = order_item.quantity
                if not reduce_quantity_in_stock(product_id, quantity):
                    flash(f'Not enough quantity in stock for {order_item.product.name}', 'danger')
                    return redirect(url_for('keranjang'))

            # Mark the session as inactive
            active_session.is_active = False

            # Commit changes to the database
            db.session.add(new_order)
            db.session.commit()

            # Clear the order items from the current session
            flask_session.pop('order_items', None)

            flash('Checkout successful', 'success')
        else:
            flash('No items in the cart to checkout', 'danger')
    else:
        flash('No active session to checkout', 'danger')

    return redirect(url_for('products'))


@app.route('/delete_item/<int:id_order_item>', methods=['POST'])
@login_required
def delete_item(id_order_item):
    # Get the order item based on id_order_item
    order_item = Order_items.query.get_or_404(id_order_item)

    # Delete the order item
    db.session.delete(order_item)
    db.session.commit()

    # Redirect back to the cart page
    flash('Item deleted successfully', 'success')
    return redirect(url_for('keranjang'))




if __name__ == "__main__":
    app.run(debug=True)

