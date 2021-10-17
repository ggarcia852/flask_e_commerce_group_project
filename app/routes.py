from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user ,logout_user, current_user, login_required
from app.forms import Ranger, UserInfoForm, LoginForm
from app.models import User, Item, Cart


@app.route('/') 
def index():
    title = 'Power Programmers Home'
    
    return render_template('index.html', title=title )



@app.route('/my_account') 
@login_required 
def my_account():     
    title = 'My Account'

    return render_template('my_account.html', title=title)



@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        # Check if username from the form already exists in the User table
        existing_user = User.query.filter_by(username=username).all()
        # If there is a user with that username, message them asking them to try again
        if existing_user:
            # Flash a warning message 
            flash(f'The username {username} is already registered. Please try again.', 'danger')
            # Redirect back to the register page
            return redirect(url_for('register'))        

        # Create a new user instance
        new_user = User(username, email, password)
        # Add that user to the database
        db.session.add(new_user)
        db.session.commit()
        # Flash a success message thanking them for signing up
        flash(f'Thank you {username}, you have successfully registered!', 'success')
        # Redirecting to the home page
        return redirect(url_for('index'))

    return render_template('register.html', title=title, form=register_form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    title= 'Login'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query our User table for a user with username
        user = User.query.filter_by(username=username).first()

        # Check if the user is None or if password is incorrect
        if user is None or not user.check_password(password):
            flash('Your username or password is incorrect', 'danger')
            return redirect(url_for('login'))

        login_user(user)

        flash(f'Welcome {user.username}. You have successfully logged in.', 'success')

        return redirect(url_for('index'))

    return render_template('login.html', title=title, login_form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/addranger', methods=['GET', 'POST'])
@login_required
def addranger():
    ranger = Ranger()
    if ranger.validate_on_submit():
        color = ranger.color.data
        skill = ranger.skill.data
        description = ranger.description.data
        image = ranger.image.data
        price = ranger.price.data

        new_ranger = Item(color, skill, description, image, price)
        db.session.add(new_ranger)
        db.session.commit()

        flash('New Ranger Added')
        return redirect(url_for('index'))
    return render_template('add_ranger.html', form=ranger)



@app.route('/rangers')
def rangers():
    title = 'The Power Pogrammers'
    rangers = Item.query.all()
    return render_template('rangers_display.html', rangers=rangers, title=title)



@app.route('/ranger_detail/<item_id>')
def ranger_detail(item_id):
    title = 'Programmer Product Page'
    ranger = Item.query.get_or_404(item_id)
    return render_template('view_ranger.html', ranger=ranger, title=title)



@app.route('/ranger_detail/<item_id>/add', methods=['POST'])
@login_required
def add_item(item_id):
    item = Item.query.get_or_404(item_id)

    new_cart = Cart(current_user.id, item_id, item.price)
    db.session.add(new_cart)
    db.session.commit()
    flash (f'You have succesfully added {item.color} to your cart!')
    return redirect(url_for('cart', item=item))


    
@app.route('/cart', methods=["GET", "POST"] )
@login_required
def cart():
    items = Item.query.join(Cart).add_columns(Item.color, Item.skill, Item.image, Item.skill, Cart.price).all()
    return render_template('cart.html', items=items)



@app.route('/cart/remove_item/<item_id>', methods=['POST'])
def remove_item(item_id):
        item = Cart.query.get_or_404(item_id)
    
        db.session.delete(item)
        db.session.commit()
        flash('Your item has been removed from your cart.', 'success')
        return redirect(url_for('cart'))