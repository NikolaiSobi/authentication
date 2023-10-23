from flask import Flask, request, render_template, redirect
from models import *
from forms import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret159"


app.app_context().push()

connect_db(app)

@app.route('/')
def homepage():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """register the user"""

    form = Register()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/secret')

    return render_template('registerForm.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    


@app.route('/secret')
def secret():
    return "secret"