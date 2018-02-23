from flask import Flask
from calla.config import Config
from flask_cors import CORS

def make_app(conf_path = None):
    '''
    Args:
        从命令行指定 config 的文件位置
    '''
    if conf_path:
        Config.monkey_patch(conf_path)

    config = Config()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Security'
    app.debug = config.server_debug or True

    from calla.views import admin_bp, article_bp, setting_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(setting_bp)

    from calla.api import article_api, setting_api, index_api, task_api
    app.register_blueprint(article_api)
    app.register_blueprint(setting_api)
    app.register_blueprint(index_api)
    app.register_blueprint(task_api)

    # CORS
    cors = CORS(app, resources={r'/api/*': {'origins': '*'} })
    return app
