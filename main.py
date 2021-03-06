from flask import Flask, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Password1!@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    post_date = db.Column(db.DateTime)

    def __init__(self, title, body, post_date=None):
        self.title = title
        self.body = body
        if post_date is None:
            post_date = datetime.utcnow()
        self.post_date = post_date

@app.route('/blog')
def blog():
    posts = Blog.query.order_by(Blog.post_date.desc()).all()
    id = request.args.get('id')
    if not id:
        return render_template('blog.html', posts=posts)
    else:
        blog = Blog.query.get(id)
        return render_template('entry.html', blog=blog)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form["body"]
        t_error = ''
        b_error = ''

        if blog_title == '':
            t_error = "Please enter a title."
        if blog_body == '':
            b_error = "Please enter something for your post."

        if not t_error and not b_error:    
            new_post = Blog(blog_title, blog_body)
            db.session.add(new_post)
            db.session.commit()
            newest_post = db.session.query(Blog).order_by(Blog.id.desc()).first()
            id = str(newest_post.id)
            return redirect("/blog?id=" + id)
        else:
            return render_template('newpost.html', t_error=t_error, b_error=b_error, blog_title=blog_title, blog_body=blog_body)
    else:
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
