from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'U\xee\xe2F\xd2\x03\xa8\x9d+\xe3\xfb5gz\xea'

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks = db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        session['email'] = email
        if user and user.password == password:
            flash("Login successful", category='message')
            return redirect('/')
        else:
            # Error message for failed login
            flash("Error: Email/Password combination not found, please check entries and try again", category='error')


    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        session['email'] = email

        # TODO Validate user data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful", category='message')
            return redirect('/')
        else:
            flash("Login successful", category='message')
    
    return render_template('register.html')

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['email']
    flash("Logout successful", category='message')
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(email=session['email']).first()
# Adding tasks to list
    if request.method == 'POST':
        task_name = request.form['task']
        owner = User.query.filter_by(email=session['email']).first()
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit()

# Show all tasks
    tasks = Task.query.filter_by(completed=False,owner=owner).all()
    completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():

# Removing tasks from list (marking them as 'Done!')
    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()
    
    return redirect('/')


# only run app if it is called, otherwise ignore
if __name__ == '__main__':
    app.run()