from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)

# INITIALIZING CKEDITOR
ckeditor = CKEditor(app)



# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


# FORM TO MAKE NEW POST
class MakePost(FlaskForm):
    title = StringField("Enter Blog Title", validators=[DataRequired()])
    subtitle = StringField("Enter Subtitle", validators=[DataRequired()])
    author = StringField("Author's name")
    img_url = StringField("Background image URL", validators=[DataRequired(), URL(message="Invalid Image URL")])
    body = CKEditorField("Post Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    all_post = BlogPost.query.all()
    posts = [post for post in all_post]
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.get(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/new_post", methods=['GET', 'POST'])
def add_new_post():
    form = MakePost()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            date=date.today().strftime("%B %d %Y"),
            body=form.body.data,
            img_url=form.img_url.data
        )
        try:
            db.session.add(new_post)
            db.session.commit()
        except IntegrityError:
            flash(f"Post with {form.title.data} already exists", 'danger')
            db.session.rollback()
        else:
            return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

# TODO: edit_post() to change an existing blog post


# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>", methods=['GET', 'POST'])
def delete_post(post_id):
    post_data = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_data)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
