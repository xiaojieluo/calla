'''
post /api/tasks  新建任务
post /api/tasks/publish 发布文章
'''
from flask import current_app, Blueprint, request, Response
from flask_restplus import Resource, Api
from calla.config import Config
import subprocess
import os
import copy

app = current_app
task_api = Blueprint('task_api', __name__, url_prefix='/api/tasks')
api = Api(task_api)

def make_config():
    ''' 根据配置文件组装 config '''
    _config = Config()
    config = _config
    print(config)
    workname = os.path.dirname(config._path)
    config.path = os.path.join(workname, config.path)
    return config

class Publish(Resource):
    '''
    发布文章
    '''
    def post(self):
        config = make_config()
        data = request.json
        msg = []
        # msg.append(Make.html(config))

        # return Response(generate())
        # p = subprocess.Popen(['pelican'])
        # s = p.wait()
        # for key, value in data.items():
        #     if key == 'ftp':
        #         msg.append(Make.ftp(**value))
        #
        #     print(value)
        return Response(Make.ftp(), 'application/octet-steam')
        print(msg)
        print("Post published")

api.add_resource(Publish, '/publish/')
