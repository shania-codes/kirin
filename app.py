from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "worst_admin"
UPLOAD_FOLDER = "static/music"
ALLOWED_EXTENSIONS = {"aac", "flac", "m4a", "mp3", "oog", "opus", "wav", "webm"} # https://en.wikipedia.org/wiki/Audio_file_format Added the ones that look familiar
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    db = sqlite3.connect("data.db")
    return db
def create_db():
    db = get_db()
    cursor = db.cursor()

    # Create tables
    ## table1
    #cursor.execute("")

    db.commit()
    db.close()
create_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)

    

    return render_template("index.html")