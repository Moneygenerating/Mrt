import os
import func
from func import pred_func
from func import load_data
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory, after_this_request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)
app.config['UPLOAD_FOLDER'] = uploads_dir


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('analyze', name=filename))

    return render_template('index.html')


@app.route('/result/<name>')
def analyze(name):
    file_path = app.config['UPLOAD_FOLDER']


    result = pred_func(load_data(app.instance_path))

    return render_template('result.html', result=result, filename=name)


@app.route('/uploads/<filename>')
def send_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_handle = open(file_path, 'rb')

    def stream_and_remove_file():
        yield from file_handle
        file_handle.close()
        os.remove(file_path)

    r = app.response_class(stream_and_remove_file())
    r.headers.set('Content-Disposition', 'attachment', filename=filename)
    return r




@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
    # потом поставить значение False когда нужно будет показать конечному пользователю
