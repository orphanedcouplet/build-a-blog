from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://build-a-blog:blog-a-build@localhost:8889/build-a-blog"
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280))
    body = db.Column(db.String(10000000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/blog", methods=["POST", "GET"])
def index():
    # TODO make it post the thing you enter
    if request.method == "POST":
        entry_title = request.form["title"]
        entry_body = request.form["body"]
        new_entry = Blog(entry_title, entry_body)
        db.session.add(new_entry)
        db.session.commit()
    
    entries = Blog.query.all()

    # TODO make error messages for if blog title or blog body is empty
    # hint: look at user-signup
    return render_template("blog.html", title="The Blog", entries=entries)

@app.route("/newpost", methods=["POST", "GET"])
def new_post():
    return redirect("/blog")

if __name__ == "__main__":
    app.run()
