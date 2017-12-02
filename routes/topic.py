from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
    request,
    abort,
)

from models.topic import Topic

from .index import current_user

main = Blueprint('topic', __name__)

import uuid

csrf_tokens = dict()


@main.route("/")
def index():
    token = str(uuid.uuid4())
    u = current_user()
    if u is None:
        return redirect((url_for('index.index')))
    csrf_tokens[token] = u.id
    ms = Topic.all()
    return render_template('topic/index.html', ms=ms, token=token, user=u)


@main.route("/<int:id>")
def detail(id):
    t = Topic.get(id)
    return render_template('topic/detail.html', topic=t)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    t = Topic.new(form, user_id=u.id)
    return redirect((url_for('.detail', id=t.id)))


@main.route("/new")
def new():
    return render_template("topic/new.html")


@main.route("/delete")
def delete():
    u = current_user()
    id = int(request.args.get('id'))
    token = request.args.get('token')
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        t = Topic.find_by(id=id)
        print(t)
        t.delete()
        return redirect(url_for('.index'))
    else:
        abort(403)
