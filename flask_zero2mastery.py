from flask import Flask, render_template

app = Flask(__name__)
print(__name__)

@app.route("/")
def hello_world():
    return render_template('.html')



@app.route("/blog")
def blogs():
    return "<p>Thoughts on blogs!</p>"


@app.route("/blog2")
def blogger():
    return "<p>Blog 2 thoughts</p>"



