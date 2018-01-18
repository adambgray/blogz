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

    return render_template('base.html',page_title="The Blog")

@app.route('/blog')
def blog():
    title = request.args.get('title')
    body = request.args.get('body')
    if title and body:
        return render_template('blogentry.html', title=title, body=body)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html',page_title="The Blog", 
        blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title and body:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('blogentry.html', title=title, body=body)
        else:
            return render_template('newpost.html', page_title="Add a new post", title=title, body=body, error='Blog must contain a title and a body.')
    else:
        return render_template('newpost.html')



if __name__ == '__main__':
    app.run()