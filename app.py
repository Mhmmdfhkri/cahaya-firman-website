from main import app, db, bcrypt, login_manager
from flask import render_template, url_for, redirect, request, flash,session as flask_session,g,abort,jsonify
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
from sqlalchemy import func
from functools import wraps
from sqlalchemy.orm import joinedload



def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Check if the current user is logged in and is an admin
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You need to log in as an admin to access this page.", "danger")
            return redirect(url_for('loginadmin'))
        return func(*args, **kwargs)
    return decorated_view

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
    
def get_product(id_product):
    return Product.query.get(id_product)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def products():

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)
    
    # Get all products
    barang_list = Product.query.all()

    # Calculate average rating for each product
    product_avg_ratings = {}
    for product in barang_list:
        product_reviews = reviews.query.filter_by(id_product=product.id_product).all()
        if product_reviews:
            total_ratings = sum(review.rating for review in product_reviews)
            average_rating = total_ratings / len(product_reviews)
            product_avg_ratings[product.id_product] = average_rating
        else:
            product_avg_ratings[product.id_product] = 0.0

    return render_template("product.html", barang_list=barang_list, user=current_user, product_avg_ratings=product_avg_ratings)

# Rute untuk menampilkan halaman detail produk berdasarkan ID produk
@app.route('/detail_product/<int:id_product>', methods=["GET", "POST"])
def detail_product(id_product):

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

    product = get_product(id_product)
    print("Product Reviews:", product.reviews)
    if request.method == "POST":
        # Check if the user is logged in
        if not current_user.is_authenticated:
            flash("You must log in to submit a review.", "danger")
            return redirect(url_for("login"))

        # Get user input from the form
        rating = int(request.form.get("rating"))
        comment = request.form.get("comment")

        # Create a new review object
        new_review = reviews(id_user=current_user.id_user, id_product=id_product, rating=rating, comment=comment)

        # Commit the review to the database
        db.session.add(new_review)
        db.session.commit()

    # Get all reviews for the product
    product_reviews = reviews.query.filter_by(id_product=id_product).all()

    # Calculate average rating
    average_rating = 0.0
    if product_reviews:
        total_ratings = sum(review.rating for review in product_reviews)
        average_rating = total_ratings / len(product_reviews)

    return render_template('detail_product.html', product=product,  reviews=product_reviews, user=current_user, average_rating=average_rating)


@app.route("/home")
def home():

    if current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

    return render_template("home.html",user = current_user)

@app.route("/loginadmin", methods=['GET', 'POST'])
def loginadmin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.is_admin:
                login_user(user)
                print("Admin logged in successfully")
                return redirect(url_for('admin_crud'))
            else:
                flash("Invalid login credentials for admin", "danger")
        else:
            flash("Invalid login credentials", "danger")
    return render_template("loginadmin.html", form=form)

@app.route("/about")
def about():

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

    return render_template("about.html",user = current_user)

@app.route("/keranjang")
def keranjang():

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

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

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

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
        SubPengiriman = 20000
        layanan = 1000
        Penanganan = 1000
        overall_pay = total_price + SubPengiriman + layanan + Penanganan
        return render_template("Checkout.html", user=current_user, order_items=order_items, total_price=total_price, overall_pay=overall_pay)

    flash("No active session to checkout", "danger")
    return redirect(url_for("keranjang"))


@app.route("/payment")
def Payment():

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

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
@admin_required
def admin_user():
    users = User.query.all()
    return render_template("admin_user.html", users=users)

@app.route("/admin_crud")
@admin_required
def admin_crud():
    barang_list = Product.query.all()
    return render_template('admin_crud.html', barang_list=barang_list)

@app.route('/admin_status')
@admin_required
def admin_status():
    orders = Order_detail.query.join(Payment_detail).all()
    return render_template("admin_status.html", orders=orders)

@app.route('/approve_payment/<int:payment_id>', methods=['POST'])
@admin_required
def approve_payment(payment_id):
    order_detail = Order_detail.query.filter_by(id_payment=payment_id).first_or_404()

    # Update order status to 'approve'
    order_detail.order_status = 'approve'

    # Reduce quantity in stock when the admin approves the order
    for order_item in order_detail.session.order_items:
        product_id = order_item.product.id_product
        quantity = order_item.quantity
        if not reduce_quantity_in_stock(product_id, quantity):
            flash(f'Not enough quantity in stock for {order_item.product.name}', 'danger')
            return redirect(url_for('admin_status'))

    # Commit the changes to the database
    db.session.commit()

    flash('Payment approved successfully', 'success')
    return redirect(url_for('admin_status'))

@app.route('/disapprove_payment/<int:payment_id>', methods=['POST'])
@admin_required
def disapprove_payment(payment_id):
    order_detail = Order_detail.query.filter_by(id_payment=payment_id).first_or_404()

    # Update order status to 'disapprove'
    order_detail.order_status = 'disapprove'

    # Commit the changes to the database
    db.session.commit()

    flash('Payment disapproved successfully', 'success')
    return redirect(url_for('admin_status'))

@app.route('/view_invoice/<int:payment_id>')
@admin_required
def view_invoice(payment_id):
    order_detail = Order_detail.query.filter_by(id_payment=payment_id).options(joinedload(Order_detail.session)).first_or_404()

    # Render the invoice template and pass the necessary data
    return render_template('invoice.html', order=order_detail, user=current_user, overall_pay=order_detail.total, total_price=order_detail.total, total_quantity=1)

# admin end

# crud

@app.route('/cust_view_invoice/<int:payment_id>')
@login_required
def cust_view_invoice(payment_id):
    order_detail = Order_detail.query.filter_by(id_payment=payment_id).options(joinedload(Order_detail.session)).first_or_404()

    # Render the invoice template and pass the necessary data
    return render_template('invoice.html', order=order_detail, user=current_user, overall_pay=order_detail.total, total_price=order_detail.total, total_quantity=1)

@app.route("/add")
@admin_required
def add():
    return render_template("add.html")

@app.route('/add_barang', methods=['POST'])
@admin_required
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
@admin_required
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
@admin_required
def delete_barang(id):
    barang = Product.query.get_or_404(id)
    db.session.delete(barang)
    db.session.commit()
    flash('Barang deleted successfully', 'success')
    return redirect(url_for('admin_crud'))


@app.route("/contact")
def contact():

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

    return "<p>Contact Us</p>"

@app.route("/profil")
@login_required
def profil():

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

    return render_template("profil.html",user=current_user)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

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

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

    logout_user()
    return redirect(url_for('login'))

@app.route('/logoutadmin', methods=['GET', 'POST'])
@admin_required
def logoutadmin():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_to_cart/<int:id_product>', methods=['POST'])
@login_required
def add_to_cart(id_product):

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

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

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

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

    if current_user.is_authenticated and current_user.is_admin:
        flash("You need to log in as a user to access this page.", "danger")
        abort(403)

    new_order = None  # Define new_order outside the if block

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
        SubPengiriman = 20000
        layanan = 1000
        Penanganan = 1000
        overall_pay = total_price + SubPengiriman + layanan + Penanganan

        # Check if there are order items to proceed
        if order_items:
            # Create a new payment_detail object
            new_payment = Payment_detail(amount=overall_pay, payment_method=request.form.get('paymentMethod'), payment_date=datetime.utcnow())
            db.session.add(new_payment)
            db.session.commit()

            # Create a new order_detail object
            new_order = Order_detail(total=overall_pay, order_status='Pending', id_payment=new_payment.id_payment, id_session=active_session.id_session)

            new_order.order_items = order_items  # Link the order_detail to the order_items

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

    # Use new_order variable here, even if it's not set in the if block
    return redirect(url_for('invoice', order_id=new_order.id_order if new_order else None))


@app.route('/delete_item/<int:id_order_item>', methods=['POST'])
@login_required
def delete_item(id_order_item):

    if  current_user.is_authenticated and current_user.is_admin:
            flash("You need to log in as a user to access this page.", "danger")
            abort(403)

    # Get the order item based on id_order_item
    order_item = Order_items.query.get_or_404(id_order_item)

    # Delete the order item
    db.session.delete(order_item)
    db.session.commit()

    # Redirect back to the cart page
    flash('Item deleted successfully', 'success')
    return redirect(url_for('keranjang'))

@app.route('/invoice/<int:order_id>', methods=['GET'])
@login_required
def invoice(order_id):

            
    # Get the order details based on order_id
    order = Order_detail.query.get_or_404(order_id)
    
    total_price = sum(order_item.quantity * order_item.product.price for order_item in order.session.order_items)
    total_quantity = sum(order_item.quantity for order_item in order.session.order_items)
    SubPengiriman = 20000
    layanan = 1000
    Penanganan = 1000
    overall_pay = total_price + SubPengiriman + layanan + Penanganan

    # Render the invoice template and pass the necessary data
    return render_template('invoice.html', order=order, user=current_user, overall_pay=overall_pay, total_price=total_price, total_quantity=total_quantity )

@app.route('/add_to_checkout/<int:id_product>', methods=['POST'])
@login_required
def add_to_checkout(id_product):
    # Get the product based on id_product
    product = Product.query.get_or_404(id_product)

    # Check if the user has an active session
    if current_user.session is None or not any(sess.is_active for sess in current_user.session):
        new_session = session(id_user=current_user.id_user, total=0)
        db.session.add(new_session)
        db.session.commit()

    # Find the active session in the list
    active_session = next(sess for sess in current_user.session if sess.is_active)

    # Check if the product is already in the checkout
    existing_order_item = Order_items.query.filter_by(id_product=id_product, id_session=active_session.id_session).first()

    # Define new_order_item outside the if block
    new_order_item = None

    if existing_order_item:
        # If the item is already in the checkout, increase the quantity
        existing_order_item.quantity += 1
    else:
        # If the item is not in the checkout, create a new order item
        quantity = int(request.form.get('quantity', 1))  # Get the quantity from the form
        new_order_item = Order_items(id_product=id_product, id_session=active_session.id_session, quantity=quantity)
        db.session.add(new_order_item)

    # Commit the changes to the database
    db.session.commit()

    # Store the order items in flask.g only if new_order_item is defined
    if new_order_item:
        g.setdefault('order_items', []).append(new_order_item)

    flash(f'{product.name} added to the checkout', 'success')
    return redirect(url_for('Checkout'))

@app.route('/myinvoice')
@login_required
def myinvoice():

    user_invoices = db.session.query(Order_detail).join(Order_detail.session).filter(session.id_user == current_user.id_user).all()

    return render_template('myinvoice.html', invoices=user_invoices)

if __name__ == "__main__":
    app.run(debug=True)

