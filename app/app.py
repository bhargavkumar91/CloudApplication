from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import os
port = int(os.environ.get("PORT", 5000))
app = Flask(__name__, static_url_path='/static')

app.debug = True
app.secret_key = "Nothing"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404
    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=port)
