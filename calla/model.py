from peewee import *
import time
import os
from calla.article import Article as Article_
import peewee
import json

db_path = os.path.join(os.getcwd(), 'calla.db')

db = SqliteDatabase(db_path)

class JsonField(CharField):
    db_field = 'JsonField'

    def python_value(self, value):
        value  = json.loads(value)
        return value

    def db_value(self, value):
        value = json.dumps(value)
        return value

class BaseModel(Model):
    class Meta:
        database = db
    @classmethod
    def init(cls):
        ''' 初始化数据库'''
        pass

    @classmethod
    def find(cls, *args, **kw):
        ''' 查找单个 '''
        try:

            item = cls.get(*args)
        except cls.DoesNotExist:
            # log
            item = None
        return item

    @classmethod
    def find_all(cls):
        ''' 查找所有 '''
        for item in cls.select():
            yield item

class Article(BaseModel):
    ''' 文章 model '''
    # 标题
    title = CharField(index = True)
    # 作者
    author = CharField(null = True)
    # 标签, 多个用逗号分隔
    tags = CharField(default = '', index = True)
    # 创建时间
    created_at = TimeField(default = time.time())
    # 更新时间
    updated_at = TimeField(null = True)
    # 发布时间
    published_at = TimeField(null = True)
    # metadata, 字典类型
    meta = JsonField(default = {})

    # def save(self, *args, **kw):
    #     ''' 重写父类 save, 转换 meta 格式为 json'''
    #     self.meta = json.dumps(self.meta)
    #     super().save(*args, **kw)

class Page(BaseModel):
    ''' 页面  model '''
    pass

class Setting(BaseModel):
    ''' 设置 Model'''
    key = CharField()
    value = CharField()

    @classmethod
    def init(cls):
        ''' 初始化数据库'''
        default_config = [
            { 'key': 'title', 'value': '我的博客' }
        ]
        for conf in default_config:
            cls.create(**conf)

class Log(BaseModel):
    name = CharField(default  ='')
    # 线程开始时间
    start_time = DateField(default = time.time())
    # 线程结束时间
    end_time = DateField(default = '')
    # 线程运行时间
    run_time = TimeField(default = 0)
    # 线程pid
    pid = IntegerField(default = -1)
    # 线程状态
    status = CharField(default = 'waiting')
    # 命令输出正文
    log = CharField(default = '')
    # 命令原文
    command = CharField(default = '')
    # 内存使用率, 用逗号分隔
    memory_percent = CharField(default  = '')
    # 内存使用， rss 实际内存， vms 虚拟内存
    memory_info = CharField(default = '')
