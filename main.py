from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():

    return render_template('base.html',title="The Blog")

@app.route('/blog')
def blog():
   # blog_id = request.args.get(blog_id)
    blogs = Blog.query.all()
    return render_template('blog.html',title="The Blog", 
        blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if blog_title and blog_body:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('blogentry.html', blog_title=blog_title, blog_body=blog_body)
        else:
            return render_template('newpost.html', title="Add a new post", blog_title=blog_title, blog_body=blog_body, error='Blog must contain a title and a body.')
    else:
        return render_template('newpost.html')



if __name__ == '__main__':
    app.run()