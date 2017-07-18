from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

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
    username = db.Column(db.String(12), unique=True)
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Index page redirects to /blog
@app.route("/")
def index():
    return redirect("/blog")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        session['username'] = username
        if user and user.password == password:
            flash("Login successful", category='message')
            return redirect('/')
        else:
# Error message for failed login
            flash("Error: Username/Password combination not found, please check entries and try again", category='error')

    return render_template('login.html', title="Login to start blogging!")

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    flash("Logout successful", category='message')
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
    
# If no specific blog selected, show all blogs

    blogs = Blog.query.order_by(desc(Blog.pub_date)).all()
    return render_template('blogs.html',title="Build-a-Blog!", 
        blogs=blogs)

# Route to page where a user can create a new post, new data adds to db

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    # Adding a new blog
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        owner = User.query.filter_by(username=session['username']).first()
        
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

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        session['username'] = username
# username and password user validation

        if len(username) == 0:
            flash("Error: please create a username between 1 and 12 characters", category='error')
        elif len(password) == 0:
            flash("Error: please create a password", category='error')

# check for existing user. If not, create new user
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                flash("Thanks, you are now signed up!", category='message')
                return redirect('/')
            else:
                flash("Login successful!", category='message')
    
    return render_template('signup.html', title="Signup to start building your own blog!")

# only run app if it is called, otherwise ignore
if __name__ == '__main__':
    app.run()