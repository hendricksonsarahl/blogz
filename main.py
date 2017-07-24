from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import hashlib
from hashutils import make_hash, check_hash

# Set up the Flask app and SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'dafa027a46710270f5ab170a2dde79da4da52482fd43bd10'

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

db = SQLAlchemy(app)

# Database model
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, content, owner, pub_date=None):
        self.title = title
        self.content = content
        self.owner = owner
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    pw_hash = db.Column(db.String(800))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_hash(password)

# Index page shows list of users
@app.route("/")
def index():
    users = User.query.all()
    return render_template('index.html',title="Blogz Authors!", 
        users=users)
    

# signup for a new user account, redirect while signed in to active session
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        session['username'] = username

# username and password user validation
        if len(username) == 0:
            flash("Error: please create a username between 1 and 15 characters", category='error')
        elif len(username) > 15:
            flash("Error: Username is too long - must be between 1 and 15 characters", category='error')
        elif len(password) == 0:
            flash("Error: please create a password between 1 and 25 characters", category='error')
        elif password != verify:
            flash("Error: password and verify entries do not match", category='error')

# check for existing user. If not, create nsew user
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                flash("Thanks, you are now signed up!", category='message')
                return redirect('/newpost')
            else:
                flash("Error: an account already exists for this username, please log in or create a new account", category='error')
    
    return render_template('signup.html', title="Signup to start building your own blog!")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        user = User.query.filter_by(username=username).first()

        if user and check_hash(password, user.pw_hash):
            flash("Login successful", category='message')
            return redirect('/newpost')
        else:
# Error message for failed login
            flash("Error: Username/Password combination not found, please check entries and try again", category='error')
            return redirect('/login')

    return render_template('login.html', title="Login to start blogging!")

# requires user login session to access newpost page
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

# Main page shows all blog posts
@app.route('/blog', methods=['POST', 'GET'])
def blog():
 
#check for query parameters
    blog_id = request.args.get('id')

    if blog_id:
        blogs = Blog.query.filter_by(id=blog_id).all()
        selected_post = Blog.query.filter_by(id=blog_id).first()
        return render_template("blogs.html", title=selected_post.title, blogs=blogs)
    
    user_id = request.args.get('user')

    if user_id:
        blogs = Blog.query.filter_by(owner_id=user_id).order_by(Blog.pub_date.desc()).all()
        if len(blogs) > 0:
            return render_template("selecteduser.html", title="{}'s Posts".format(blogs[0].owner.username), blogs=blogs)
        else:
            return render_template("selecteduser.html", title="This user hasn't posted yet!", blogs=blogs)

# If no dynamic selected post or selected user page, display all blog posts

    blogs = Blog.query.order_by(desc(Blog.pub_date)).all()
    return render_template('blogs.html', title="Blogz!", 
        blogs=blogs)

# Route to page where a user can create a new post, new data adds to db

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

# Adding a new blog
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        owner = User.query.filter_by(username=session['username']).first()
        
# user validation to check for title and content
        if len(title) == 0:
            flash("Error: Please enter a title for your blog!", category='error')
            return redirect('/newpost')
        if len(content) == 0:
            flash("Error: Please create content for your blog!", category='error')
            return redirect('/newpost')
        else:
            new_blog = Blog(title, content, owner)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id=" + str(new_blog.id))
            flash("New blog successfully created!", category='message')
            

    return render_template('newpost.html', title="Create a new blog post!")

# logout / end user session
@app.route('/logout')
def logout():
    del session['username']
    flash("Logout successful", category='message')
    return redirect('/blog')

# only run app if it is called, otherwise ignore
if __name__ == '__main__':
    app.run()