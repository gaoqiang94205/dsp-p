# -*- coding:utf-8 -*-

import json
import logging
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from flask import Flask, Response
from api_loader import load_api
from dsp.error.errors import APIException
from dsp.moudle_add import load_moudle
from settings import SOURCE_ROOT, setup_logging

log = logging.getLogger(__name__)

def create_app(name=None):
    setup_logging()
    app = Flask(name or 'App', template_folder=os.path.join(SOURCE_ROOT, 'templates'))
    app.config.root_path = os.path.dirname(os.path.abspath(__file__))
    app.config.from_pyfile('settings.py')
    load_api(app)
    load_moudle(app)
    #CORS(apps)
    return app

app = create_app()

@app.errorhandler(APIException)
def handler_api_exception(error):
    print '进入exception'
    return Response(json.dumps({'message':unicode(error.message),'error':unicode(error.error)}),
                    content_type='application/json',status='500')

@app.errorhandler(Exception)
def haddler_no_defination(e):
    return Response(json.dumps({'message':unicode(e.message),'error:':'服务端发生错误'}),content_type='application/json', status='500')

if __name__ == '__main__':

    app.run('0.0.0.0', 51, debug=True, use_reloader=True)

