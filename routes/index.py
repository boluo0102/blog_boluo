from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    send_from_directory,
)
from models.user import User
from werkzeug.utils import secure_filename
from config import user_file_director
import os

main = Blueprint('index', __name__)


def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route("/profile")
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import allow_list
    return suffix in allow_list


@main.route("/addimg", methods=["POST"])
def addimg():
    u = current_user()
    if u is None:
        return redirect(url_for('.login'))
    else:
        file = request.file['file']
        filename = secure_filename(file.filename)
        if allow_file(filename) is True:
            file.save(os.path.join(user_file_director, filename))
            u.user_image = filename
            u.save()
    return redirect(url_for(".profile"))


@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(user_file_director, filename)
