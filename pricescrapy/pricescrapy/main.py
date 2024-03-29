import configparser
import os
import time
import socket
import status
from flask import Flask, flash, request, redirect, render_template, Markup
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = '/tmp/uploads'

app = Flask(__name__)
app.secret_key = "@$#secret%key&"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

auth = HTTPBasicAuth()

users = {
    "prof": generate_password_hash("torg"),
    "admin": generate_password_hash("nimda")
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@auth.login_required
def upload_form():
    shop_list = {}
    config = configparser.ConfigParser()
    config.read('shops.cfg')
    for key, value in config.items('Shops'):
        shop_list[key] = value
    state = status.status()
    flash(Markup(state))
    return render_template('upload.html', shop_list=shop_list)


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # edit the config file
        config = configparser.ConfigParser()
        config.read('shops.cfg')
        for key, value in config.items('Shops'):
            if not(request.form.get(key)):
                config.set("Shops", key, '0')
            else:
                config.set("Shops", key, '1')
                print(key)
        with open('shops.cfg', "w") as config_file:
            config.write(config_file)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Не выбран файл')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            # filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            link = '/static/result{}.xlsx'.format(timestamp)
            xlink = '/static/result_p{}.xlsx'.format(timestamp)
            fn = 'in{}.{}'.format(timestamp, ext)
            print(file.filename, fn)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
            flash(Markup('Файл {} успешно загружен. По этой <a href="{}">ссылке</a> через некоторое время,  \
                        зависящее от объема входного файла и числа выбранных магазинов, \
                        вы сможете скачать файл результата. \
                        <a href="{}">Здесь будет доступна сводная таблица.</a> '.format(fn, link, xlink)))
            return redirect('/')
        else:
            flash('Разрешенный тип файла: xls, xlsx')
            return redirect(request.url)


if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    app.run(host=ip)
