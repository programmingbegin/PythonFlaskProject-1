from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts2.db'
db = SQLAlchemy(app)
class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable = False)
    posted_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "Blog Post" + str(self.id)


@app.route('/home/<string:name>',methods = ['GET'])
def hello_world(name):  # put application's code here
    return 'Hello ' + name

@app.route('/',methods  = ["GET"])
def first_webpage():
    return render_template('index.html')

@app.route('/posts', methods = ['GET','POST'])
def posts():
    return render_template('posts.html')

@app.route("/Posts2", methods = ["GET","POST"])
def Posts2():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["content"]
        post_author = request.form['author']
        new_post = Blogs(title = post_title, content = post_content, author =   post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/Posts2")
    else:
        all_posts = Blogs.query.all()
        return  render_template("Posts2.html", posts = all_posts)
@app.route("/delete/<int:id>")
def deletion(id):
    delete_post = Blogs.query.get_or_404(id)
    db.session.delete(delete_post)
    db.session.commit()
    return redirect("/Posts2")

@app.route("/Posts2/edit/<int:id>", methods = ['GET','POST'])
def edit_dist(id):
    edit_post = Blogs.query.get_or_404(id)
    if request.method == "POST":

        edit_post.title = request.form['title']
        edit_post.author = request.form['author']
        edit_post.content = request.form['content']
        db.session.commit()
        return redirect('/Posts2')
    else:
        return render_template("Edit.html", post = edit_post)


@app.route('/Posts2/create', methods=['GET', 'POST'])
def create():
    if request.method=='POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Blogs(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/Posts2')
    else:
        return render_template('Create_Posts.html')

if __name__ == '__main__':
    app.run(debug=True)
