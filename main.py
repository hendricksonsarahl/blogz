from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

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
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, content, pub_date=None):
        self.title = title
        self.content = content
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date


# Index page redirects to /blog
@app.route("/")
def index():
    return redirect("/blog")

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


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    # Adding a new blog
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if len(title) == 0:
            flash("Error: Please enter a title for your blog!", category='error')
            return redirect('/newpost')
        if len(content) == 0:
            flash("Error: Please create content for your blog!", category='error')
            return redirect('/newpost')
        else:
            new_blog = Blog(title, content)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id=" + str(new_blog.id))
            flash("New blog successfully created!", category='message')
            

    return render_template('newpost.html', title="Create a new blog post!")



# only run app if it is called, otherwise ignore
if __name__ == '__main__':
    app.run()