from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

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

@app.route("/blog", methods=["GET"])
def index():
    
    entry_id = request.args.get("id")

    if entry_id:
        # how do I access the title of the blog object already created <IN THE DATABASE> at id=[num]?
        # <> : how do i query the database for id=[num] and related info?
        blog_entry = Blog.query.filter_by(id=entry_id).first()
        entry_title = blog_entry.title
        entry_body = blog_entry.body

        return render_template("blog-entry.html", entry_title=entry_title, entry_body=entry_body)

    else:
        entries = Blog.query.order_by(desc(Blog.id)).all()
        return render_template("blog.html", title="The Blog", entries=entries)


    # TODO handle GET request with query params
    # (go to individual blog-entry template)

    # URL format: ./blog?id=6
    # GET request param: form_value = request.args.get("param_name")
    # boils down to: /action_page?form_value={{request.args.get("param_name")}}
    # so: /blog?id={{num}}
    # id = request.args.get("num")




@app.route("/newpost", methods=["POST", "GET"])
def new_post():
    # TODO make error messages for if blog title or blog body is empty
    # hint: look at user-signup

    if request.method == "POST":
        entry_title = request.form["title"]
        entry_title_error = ""
        entry_body = request.form["body"]
        entry_body_error = ""

        # validate title
        if not entry_title:
            entry_title_error = "Your post must have a title!"
        
        # validate body
        if not entry_body:
            entry_body_error = "Your post must have text!"
        
        if not entry_title_error and not entry_body_error:
        # TODO make it post the thing you entered
            new_entry = Blog(entry_title, entry_body)
            db.session.add(new_entry)
            db.session.commit()
            entry_id = new_entry.id
            return redirect("/blog?id={}".format(entry_id))
        else:
            return render_template(
            "newpost.html", 
            entry_title_error=entry_title_error, 
            entry_body_error=entry_body_error
            )


    return render_template("newpost.html")

    #TODO fix the following bug:
    # "return redirect('/blog')" >> can't see form to enter a new entry
    # "return render_template('newpost.html')" >> doesn't redirect to /blog after posting entry
    # probably needs a conditional?
    



if __name__ == "__main__":
    app.run()
