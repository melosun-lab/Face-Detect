import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename
from gcp import upload_blob
from automl import predict_image_classification_sample

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            upload_blob("gcp_webapp_bucket", path, filename)
            #detect_text(path)
            predict_image_classification_sample("cloud-computing-311121", "3526371284789231616", path)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('test.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)