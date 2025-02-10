from flask import Blueprint, redirect, render_template

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    return redirect('/home')

@auth_bp.route('/logout')
def logout():
    return render_template('logout.html')

@auth_bp.route('/register')
def register():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register_post():
    # registration code goes here
    return redirect('/home')
