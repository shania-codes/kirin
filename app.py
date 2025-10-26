from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "worst_admin"
UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = {"flac", "mp3"} # https://en.wikipedia.org/wiki/Audio_file_format https://www.iana.org/assignments/media-types/media-types.xhtml#audio
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Create upload folder if it doesn't exist

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    db = sqlite3.connect("data.db")
    return db
def create_db():
    db = get_db()
    cursor = db.cursor()

    # Create tables
    ## "Queue" (There MUST be a better way to do this?)
    #cursor.execute("CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY AUTOINCREMENT, file TEXT NOT NULL)")

    db.commit()
    db.close()
create_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)
        file = request.files["audio"]
        if file.filename == "": # if no file is uploaded
            filename = None 
        elif file and allowed_file(file.filename): # If the file exists and it has an allowed name and file extension then save it
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # TODO make sure a file with the same name doesn't exist and get's replaced by new file (this also wastes bandwidth)


    

    return render_template("index.html", files=get_uploaded_files())


# Other Functions
def get_uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            files.append(filename)
    return files

get_uploaded_files()