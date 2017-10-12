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

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("blogscroll.html")


if __name__ == "__main__":
    app.run()
