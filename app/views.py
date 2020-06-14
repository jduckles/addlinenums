import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
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
    return '''
    <!doctype html>
    <head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"></head>
    <title>Add Linenumbers to Word Documents</title>
    <div class="container">
    <div class="jumpotron">
    <h1 class="display-4">Upload a File</h1>
    <p class="lead">Upload a Word Document and it will be converted to have line-numbers and be sent back to you</p>
    <form method=post enctype=multipart/form-data>
    <div class="form-group">
    <div class="custom-file">
        <input type=file  class="custom-file-input" name=file id="customFile">
  <label class="custom-file-label" for="customFile">Choose file</label>
    </div>
    </div>
    <div class="form-group">
    <input type=submit class="btn btn-primary" value=Upload>
    </div>
    </div>
    </form>
    </div>
    </div>
 <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>

<script type="application/javascript">
    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0].name;
        $('.custom-file-label').html(fileName);
    });
</script>
'''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/')
def hello_world():
    return("Hello world")
