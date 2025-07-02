import os
import sys 
import gunicorn
loglevel = os.environ.get('LOGLEVEL', 'info').lower()
errorlog = os.environ.get('GUNICORN_ERRORLOG', '-') # stderr
accesslog = os.environ.get('GUNICORN_ACCESSLOG', '-') # stdout, but overridden if app has own logging config
access_log_format = '%(t)s %(p)s %(h)s %(l)s %(u)s  "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
if sys.platform == 'linux':
    worker_tmp_dir = "/dev/shm"
graceful_timeout = int(os.environ.get('GUNICORN_GRACEFUL_TIMEOUT', '120'))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
keepalive = int(os.environ.get('GUNICORN_KEEPALIVE', '5')) 
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:80')
gunicorn.SERVER = os.environ.get('GUNICORN_SERVER', 'Server')
