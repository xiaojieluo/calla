import sys, os
import re
from unipath import Path
import tempfile
import importlib
import pprint
import json
import toml
from calla.model import Setting
import types

here = os.path.abspath(os.path.dirname(__file__))

class Config(dict):
    ''' config 类
    attribute only read , cannot modified
    '''
    _path = None
    # 默认配置， 实例化之后创建
    # _default = None
    # TODO
    # 暂时无法像下面这样使用， 待修复
    # config.get('date_format').get('zh_cn')

    def get(self, key, default = None):
        if key in self:
            data = self[key]
            # data = super().__getitem__(key)
        elif key in self._default:
            data = self._default.get(key)
        else:
            data = default

        if isinstance(data, dict):
            data = self.__class__(data)
        return data
        # if data:
        #     if isinstance(data, dict):
        #         data = self.__class__(data)
        #     return data
        # return default

    def __getattr__(self, key):
        return self.get(key)

    # def __getitem__(self, key):
    #     if key in self._default:
    #         return super().__getitem__(key)

    def set(self, key, value):
        self.update({key: value})

    def __setattr__(self, key, value):
        self.set(key, value)

    def save(self):
        ''' 保存配置到 self._path '''
        data = {k: v for k, v in self.items() if k[0] != '_'}
        with open(self._path, 'w') as fp:
            toml.dump(data, fp)
        return True

    def delete(self, key):
        '''
        删除配置
        Args:
            key: 要删除的 key
        '''
        if key in self:
            del self[key]

    @classmethod
    def load(cls, path):
        ''' 静态变量， 从 toml 文件中加载配置并注入 Config 类中。 '''
        # if path is None and cls._path:
        #     path = cls._path
        config = toml.load(path, cls)
        instance = cls()
        instance.update(config)
        instance.__dict__['_path'] = path
        return instance

    @classmethod
    def monkey_patch(cls, path):
        cls._path = path

    def __delattr__(self, key):
        return self.__delitem__(key)

    def __delitem__(self, key):
        if key in self:
            self.pop(key)

def make_config(path = None, raw = False):
    ''' 根据配置文件组装 config
    并且用用户自定义配置覆盖默认配置
    raw:
        是否只返回用户定义的配置， 默认 False
    '''
    if path is None:
        if Config._path is None:
            path = os.path.join(os.getcwd(), 'calla.toml')
        else:
            path = Config._path

    config = Config.load(path)
    # 注入默认配置
    default_conf_path = os.path.join(here, 'config/default.toml')
    config._default = Config.load(default_conf_path)

    return config
