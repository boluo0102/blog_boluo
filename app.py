from flask import Flask
import config

app = Flask(__name__)

app.secret_key = config.secret_key

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
app.register_blueprint(index_routes)
app.register_blueprint(topic_routes,url_prefix = '/topic')
app.register_blueprint(reply_routes,url_prefix = '/reply')

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
