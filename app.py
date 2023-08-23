import csv
import io
import psycopg
import os

from flask import Flask, render_template, flash, request, redirect, url_for

pg_uri = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ampdelete")
conn_dict =  psycopg.conninfo.conninfo_to_dict(pg_uri)
with psycopg.connect(**conn_dict) as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS amplitude (amplitude_id TEXT PRIMARY KEY)")
        cur.execute("CREATE TABLE IF NOT EXISTS jobs (schedule TEXT PRIMARY KEY)")
        conn.commit()

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.getenv("SECRET_KEY")

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/")
def amp_get():
    return render_template('index.html')


@app.post("/")
def amp_post():
    project_secret = request.form['project_secret']
    if project_secret == "":
        flash('No project secret')
        return redirect(request.url)
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    filename = file.filename
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(filename):
         with io.TextIOWrapper(file) as fh:
             reader = csv.DictReader(fh)
             next(reader, None)  # skip the headers
             for row in reader:
                 print(row)
                 amplitude_id = row["amplitude_id"]
                 with psycopg.connect(**conn_dict) as conn:
                     with conn.cursor() as cur:
                         cur.execute("INSERT INTO amplitude (amplitude_id) VALUES (%s)", (amplitude_id))
                         conn.commit()
    return redirect(url_for('amp_get', name=filename))
