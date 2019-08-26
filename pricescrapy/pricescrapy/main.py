import os
# import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import time

ALLOWED_EXTENSIONS = set(['txt', 'pdf', ])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Не выбран файл')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            link = '/static/result{}.csv'.format(timestamp)
            fn = 'in{}.txt'.format(timestamp)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
            flash('Файл {} успешно загружен. По этой <a href="{}">ссылке</a> через несколько минут \
                   вы сможете скачать файл результата.'.format(fn, link))
            return redirect('/')
        else:
            flash('Разрешенный тип файла: txt')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host="167.71.37.44")
