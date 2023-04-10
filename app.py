import os.path
from datetime import datetime

from flask import Flask, g, render_template, request, send_from_directory
from humanize import naturaldelta
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.debug = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.before_request
def record_upload_time():
    g.start_time = datetime.now()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            upload_time = naturaldelta(datetime.now() - g.start_time)
            upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return render_template(
                'index.html',
                filename=filename,
                upload_time=upload_time,
                upload_date=upload_date
            )
    return render_template('index.html')


@app.route('/download/<path:filename>/')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
