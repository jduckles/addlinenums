import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import subprocess
from app import app

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'txt', 'odf','md','docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key=os.environ['SECRET_KEY']


def pandoc(arguments, cwd=None):
    PANDOC="/usr/bin/pandoc"
    command = list()
    command.append(PANDOC)
    command = command + arguments
    print("Running {}".format(command))
    subprocess.run(command, cwd=cwd)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            full_filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)

            pandoc([full_filename,'--reference-doc=/app/templates/line-numbers.docx', '-o', full_filename], cwd=UPLOAD_FOLDER)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("upload_form.html",
            title="Add Line Numbers",
            help_text="Upload a Word Document and it will be converted to have line-numbers and be sent back to you"]
            )


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/')
def hello_world():
    return("Hello world")
