from flask import Blueprint, render_template, request, redirect, flash 
from werkzeug.security import check_password_hash 
from flask_login import login_user, logout_user 


# Internal imports
from rangers_shop.models import User, db 
from rangers_shop.forms import RegisterForm, LoginForm



#instantiate our blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates') #template folder is navigating to where html files are located


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    registerform = RegisterForm()
# Save form responses
    if request.method == 'POST' and registerform.validate_on_submit():
        first_name = registerform.first_name.data 
        last_name = registerform.last_name.data 
        username = registerform.username.data 
        email = registerform.email.data 
        password = registerform.password.data 
        admin_password = registerform.admin_password.data

        print(email, password, username)


        if User.query.filter(User.username == username).first():
            flash(f"Username already exists. Please Try Again", category='warning')
            return redirect('/signup')
        if User.query.filter(User.email == email).first():
            flash("Email already exists. Please Try Again", category='warning')
            return redirect('/signup')
        
        # Will encrypt this better later
        if admin_password == 'Sneaky':
            
            user = User(username, email, password, first_name, last_name) 

            db.session.add(user) #like "git add ."
            db.session.commit() #like "git commit"


            flash(f"You have successfully registered user {username}", category='success')
            return redirect('/signin')
        else:
            flash(f"Invalid Security Key", category='warning')
            return redirect('/signup')
    
    return render_template('signup.html', form=registerform )


@auth.route('/signin', methods=['GET', 'POST'])
def signin():

    loginform = LoginForm()


    if request.method == 'POST' and loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data 
        print("login info", email, password)

        user = User.query.filter(User.email == email).first()


        if user and check_password_hash(user.password, password): 
            
            login_user(user) 
            flash(f"Successfully logged in {email}", category='success') 
            return redirect('/') 
        else:
            flash("Invalid Email or Password, Please Try Again", category='warning')
            return redirect('/signin')
    
    return render_template('signin.html', form=loginform )


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')