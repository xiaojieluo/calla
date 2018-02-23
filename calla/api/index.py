from flask import current_app, Blueprint, request, Response
from flask_restplus import Resource, Api
from calla.config import Config
import subprocess
import os
import copy

app = current_app
index_api = Blueprint('index_api', __name__, url_prefix='/api')
api = Api(index_api)

def make_config():
    ''' 根据配置文件组装 config '''
    _config = Config()
    config = _config
    print(config)
    workname = os.path.dirname(config._path)
    config.path = os.path.join(workname, config.path)
    return config

class Make(object):

    @classmethod
    def html(cls, config, pelican_opts = ''):
        ''' 生成 html '''
        # print(config._path)

        dirname = os.path.dirname(config._path)
        print(dirname)
        input_dir = config.path
        output_dir = config.output_path
        conf_file = config._path
        print(config.path)
        p = subprocess.Popen(['pelican', input_dir, '-o', output_dir, '-s',
            conf_file], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

        stdout, stderr = p.communicate()
        return stdout, stderr

    @classmethod
    # def ftp(cls, host, user, password, target_dir):
    def ftp(cls):
        ''' 发布到 ftp '''
        config = make_config()
        output_path = config.output_path
        # lftp ftp://$(FTP_USER):$(FTP_PASSWORD)@$(FTP_HOST) -e "mirror -R $(OUTPUTDIR) $(FTP_TARGET_DIR) ; quit"
        # info = 'ftp://{user}:{password}@{host}'.format(user=user, password=password, host=host)
        # mirror = 'mirror -R {output_dir} {target_dir} ; quit'.format(output_dir=output_path, target_dir = target_dir)
        # p = subprocess.Popen(['lftp', info, '-e', mirror],
        #     stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        #     )
        p = subprocess.Popen(['ping', '-c', '8', 'www.baidu.com'],
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            )

        while True:
            line = p.stdout.readline()
            if not line:
                break;
            yield line
            # print(line)



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

class Build(Resource):
    ''' 编译
    '''
    def post(self):
        args = request.json
        print(request.form)
        print("Build")

api.add_resource(Publish, '/publish/')
api.add_resource(Build, '/build/')
