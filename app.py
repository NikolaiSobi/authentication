from flask import Flask, request, render_template, redirect, session, flash
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
        if User.query.filter(User.username == form.username.data).first():
            flash("Username already exists!", "error")
            return render_template('registerForm.html', form=form)
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed = hashed.decode('utf-8')
        new_user = User(username=username, password=hashed, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(f'/user/{username}')

    return render_template('registerForm.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username'] != None:
        if User.query.filter(User.username == request.form['username']).first():
            session.pop('user', None)
            current_user = User.query.filter(User.username == request.form['username']).first()
            password = request.form['password']

            if bcrypt.checkpw(password.encode('utf-8'), current_user.password.encode('utf-8')):
                session['user'] = request.form['username']

                return redirect(f"/user/{request.form['username']}")



    return render_template('loginForm.html')

@app.route('/logout')
def logout():
    session.pop('user')

    return redirect('/login')
    


@app.route('/user/<username>', methods=['GET', 'POST'])
def secret(username):
    if "user" in session:
        username = User.query.filter(User.username == username).first()
        feedback = Feedback.query.all()
        return render_template('/user.html', username=username, feedback=feedback)
    
    return redirect('/login')

@app.route('/user/<username>/delete', methods=['POST'])
def delete_user(username):
    if "user" in session:
        user = User.query.filter(User.username == username).first()
        db.session.delete(user)
        db.session.commit()
        session.pop('user')
    
        return redirect('/')
    
    return redirect('/login')

@app.route('/user/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if "user" in session:
        user = User.query.filter(User.username == username).first()

        if request.method == 'POST':
            title = request.form['title']
            feedback = request.form['feedback']
            post = Feedback(title=title, content=feedback, username=username)
            db.session.add(post)
            db.session.commit()
            return redirect(f'/user/{username}')
        
        return render_template('addFeedback.html', user=user)
    
    return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):

    if "user" in session:
        feedback = Feedback.query.get(feedback_id)

        if request.method == 'POST':
            feedback.title = request.form['title']
            feedback.content = request.form['feedback']
            db.session.commit()
            return redirect(f'/user/{feedback.username}')

        return render_template('updateFeedback.html', feedback=feedback)
    
    return redirect('/login')

@app.route('/feedback/<int:feedback_id>/delete', methods=['GET','POST'])
def delete_feedback(feedback_id):

    if "user" in session:
        feedback = Feedback.query.get(feedback_id)
        username = feedback.username
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/user/{username}')
    
    return redirect('/login')