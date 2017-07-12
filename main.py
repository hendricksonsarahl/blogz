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

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))

    def __init__(self, title, content):
        self.title = title
        self.content = content


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

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    # Adding a new blog
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_blog = Blog(title, content)
        db.session.add(new_blog)
        db.session.commit()
        flash("New blog successfully created!", category='message')
        return redirect('/blog')

    return render_template('newpost.html')


@app.route('/blog', methods=['POST', 'GET'])
def index():

# Show all blogs 
    blogs = Blog.query.all()
    return render_template('blogs.html',title="Build-a-Blog!", 
        blogs=blogs)


# only run app if it is called, otherwise ignore
if __name__ == '__main__':
    app.run()