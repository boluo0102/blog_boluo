#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import app


sys.path.insert(0, abspath(dirname(__file__)))
application = app.app

"""
建立一个软连接
ln -s /var/www/blog_boluo/blog_boluo.conf /etc/supervisor/conf.d/blog_boluo.conf

ln -s /var/www/blog_boluo/blog_boluo.nginx /etc/nginx/sites-enabled/blog_boluo



➜  ~ cat /etc/supervisor/conf.d/blog_boluo.conf

[program:blog_boluo]
command=/usr/local/bin/gunicorn wsgi -c gunicorn.config.py
directory=/var/www/blog_boluo
autostart=true
autorestart=true




/usr/local/bin/gunicorn wsgi
--bind 0.0.0.0:2000
--pid /tmp/blog_boluo.pid
"""