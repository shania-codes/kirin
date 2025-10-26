from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import os
from werkzeug.utils import secure_filename
import io
import zipfile

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
    ## Song list
    cursor.execute("CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL)")

    ## song_tags
    cursor.execute("CREATE TABLE IF NOT EXISTS song_tags (song_id INTEGER, tag_id INTEGER, FOREIGN KEY (song_id) REFERENCES songs(id), FOREIGN KEY (tag_id) REFERENCES tags(id))")

    ## Tags
    cursor.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT NOT NULL UNIQUE)")

    db.commit()
    db.close()
create_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("form") == "new_song":
            file = request.files["audio"]
            if file.filename == "": # if no file is uploaded
                filename = None 
            elif file and allowed_file(file.filename): # If the file exists and it has an allowed name and file extension
                filename = secure_filename(file.filename)

                # Make sure a file with the same name doesn't exist and get replaced
                if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"],filename)):
                    flash("File already exists")
                    return redirect(url_for("index"))

                # Save details to DB
                db = get_db()
                cursor = db.cursor()

                cursor.execute("INSERT INTO songs (filename) VALUES (?)", (filename,))

                db.commit()
                db.close()

                # Save file to server
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash((str(filename)+" saved!"))         

        if request.form.get("form") == "add_tag_to_song":
            filename = request.form["file"]
            tag = request.form["tag"].strip()

            if not tag:
                flash("No tag was entered")
                return redirect(url_for("index"))

            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT id FROM songs WHERE filename = ?", (filename,))
            song = cursor.fetchone()
            if song == None: # Is this pointless, song will never be None unless user submits a form with incorrect filename on purpose?
                flash("Song not found in DB, try deleting it and reuploading it.")
                db.commit()
                db.close()
                return redirect(url_for("index"))
            
            song_id = song[0]

            cursor.execute("SELECT id FROM tags WHERE tag = ?", (tag,))
            existing_tag = cursor.fetchone()
            
            
            if existing_tag == None: # No other songs have that tag yet
                cursor.execute("INSERT INTO tags (tag) VALUES (?)", (tag,)) # Create tag
                tag_id = cursor.lastrowid
                flash(("Created new tag: "+ str(tag)))
                                
            else: # Tag exists, add link (idk what to call it)
                tag_id = existing_tag[0]

            # If song already has tag
            cursor.execute("SELECT * FROM song_tags WHERE song_id = ? AND tag_id = ?", (song_id, tag_id, ))
            already_added = cursor.fetchone()
            if already_added:
                flash((str(filename)+" already has tag: "+str(tag)))
            else:
                cursor.execute("INSERT INTO song_tags (song_id, tag_id) VALUES (?, ?)", (song_id, tag_id))
                flash("Tag: "+ str(tag) +" added to file: "+str(filename))

            db.commit()
            db.close()
            
        if request.form.get("form") == "delete_song":
            filename = request.form["file"]

            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT id FROM songs WHERE filename = ?", (filename, ))
            song = cursor.fetchone()

            if song:
                song_id = song[0]

                # Delete added tags
                cursor.execute("DELETE FROM song_tags WHERE song_id = ?", (song_id,))
                # Delete song in DB
                cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
                db.commit()
                db.close()
                # Delete song file
                if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
                    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    flash("Song deleted.")

            else:
                flash("Song not found.") # Useless?

        if request.form.get("form") == "delete_tag":
            tag_id = request.form["tag_id"]

            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM song_tags WHERE tag_id = ?", (tag_id))
            cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id))
            db.commit()
            db.close()
            flash("Tag deleted.")


    # Filtering Songs/Audio files
    filter_tag = request.args.get("filter_tag")
    match_mode = request.args.get("match_mode", "any")

    if filter_tag:
        tag_list = [t.strip() for t in filter_tag.split(",") if t.strip()]
        if match_mode == "all":
            files = get_songs_by_multiple_tags(tag_list) # songs with all selected tags
        else: # match_mode == any
            files = get_songs_by_tags(tag_list) # only songs with these tags
    else:
        files = get_uploaded_files() # all songs


    return render_template("index.html", files=files, tags=get_all_tags(), filter_tag=filter_tag, match_mode=match_mode)


@app.route("/backup")
def backup():
    file = io.BytesIO()
    with zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(UPLOAD_FOLDER):
            if allowed_file(filename): # so that background.png isn't included or any other future static files
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                zf.write(file_path, arcname=filename)
    file.seek(0)

    return send_file(file, mimetype="application/zip", as_attachment=True, download_name="files.zip")

@app.route("/download/<filename>")
def download_song(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)



# Other Functions
def get_uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            files.append(filename)
    return files


def get_all_tags():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, tag FROM tags")
    tags = cursor.fetchall()
    db.close()
    return tags


def get_songs_by_tags(tags): # Includes all songs with any 1 of the tags
    db = get_db()
    cursor = db.cursor()

    placeholders = ",".join("?" * len(tags))

    query = f"""
        SELECT DISTINCT s.filename 
        FROM songs s
        JOIN song_tags st ON s.id = st.song_id
        JOIN tags t ON st.tag_id = t.id
        WHERE t.tag IN ({placeholders})
    """
    cursor.execute(query, tags)
    results = [row[0] for row in cursor.fetchall()]
    db.close()
    return results

def get_songs_by_multiple_tags(tags): # Includes songs with all selected tags
    db = get_db()
    cursor = db.cursor()

    placeholders = ",".join("?" * len(tags))
    query = f"""
        SELECT s.filename
        FROM songs s
        JOIN song_tags st ON s.id = st.song_id
        JOIN tags t ON st.tag_id = t.id
        WHERE t.tag IN ({placeholders})
        GROUP BY s.id
        HAVING COUNT(DISTINCT t.tag) = ?
    """
    cursor.execute(query, (*tags, len(tags)))
    results = [row[0] for row in cursor.fetchall()]
    db.close()
    return results