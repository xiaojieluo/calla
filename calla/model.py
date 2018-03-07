from peewee import *
import time
import os
from calla.article import Article as Article_
import peewee
import json
from playhouse.shortcuts import model_to_dict
import datetime

db_path = os.path.join(os.getcwd(), 'calla.db')

db = SqliteDatabase(db_path, pragmas = (
    # 开启 sqlite3 外键
    ('foreign_keys', 'on'),
    ('cache_size', -16000)
    ))

class JsonField(CharField):
    db_field = 'JsonField'

    def python_value(self, value):
        value  = json.loads(value)
        return value

    def db_value(self, value):
        value = json.dumps(value)
        return value

class ListField(CharField):
    db_field = 'ListField'

    def python_value(self, value):
        value = value.split(',')
        # print(value)
        value  = [i.strip() for i in value]
        return value

    def db_value(self, value):
        if isinstance(value, list):
            value = [i.strip() for i in value]
            value = ','.join(value)
            # value = [i for i in 'value']
        return value

class BaseModel(Model):
    class Meta:
        database = db

    def to_dict(self):
        ''' model to dict'''
        return model_to_dict(self)

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
    # author = CharField(null = True)
    # authors = ListField(default = '', index = True)
    # 标签, 多个用逗号分隔
    # tags = CharField(default = '', index = True)
    # tags = ListField(default = '', index = True)
    # 文章正文
    content = TextField(default = '')
    # 文章状态, published or draft
    status = CharField(default = 'draft')
    # 创建时间
    created_at = DateTimeField(default = datetime.datetime.now())
    # 更新时间
    updated_at = DateTimeField(null = True)
    # 发布时间
    published_at = DateTimeField(null = True)

    @classmethod
    def create(cls, *args, **kw):
        '''
        重写create, 在插入文章之后插入 meta
        '''
        article = super().create(*args, **kw)
        # 写入 Authors
        authors = kw.pop('authors')
        if isinstance(authors, str):
            authors = authors.split(',')
        for author in authors:
            Author.insert(name = author, article = article).execute()

        # 写入 Tags
        tags = kw.pop('tags', [])
        if tags:
            if isinstance(tags, str):
                tags = tags.split(',')
            for tag in tags:
                Tag.insert(name = tag.strip(), article = article).execute()

        for k, v in kw.items():
            if not hasattr(Article, k):
                Meta.insert(article = article, key = k, value = v).execute()


    @classmethod
    def split_meta(cls, **kw):
        '''
        从传入的参素中提取 meta， 返回元组
        '''
        meta = {}
        no_meta = {}
        for key, value in kw.items():
            if not hasattr(cls, key):
                meta[key] = value
            else:
                no_meta[key] = value

        return no_meta, meta

    def to_dict(self):
        ''' 重写父类 to_dict'''
        dict_data = super().to_dict()
        # meta
        for meta in self.meta:
            dict_data.update({ meta.key : meta.value })

        # tags
        tags = [tag.name for tag in self.tags]
        dict_data.update({'tags': tags})

        return dict_data

    def save(self, *args, **kw):
        '''重写父类 save, 转换 meta 数据'''
        print(self.meta)
        super().save(*args, **kw)

    @classmethod
    def find_by_id(cls, id):
        try:
            instance = super().get_by_id(id)
        except cls.DoesNotExist:
            instance = None
        return instance

class Meta(BaseModel):
    ''' article's metadata model'''
    key = CharField()
    value = CharField(default = '')
    article = ForeignKeyField(Article, backref = 'meta', on_delete = "CASCADE", on_update = "CASCADE")

class Tag(BaseModel):
    ''' article's tags model'''
    name = CharField()
    article = ForeignKeyField(Article, backref = 'tags', on_delete = 'CASCADE', on_update = 'CASCADE')

class Page(BaseModel):
    ''' pages model'''
    pass

class Author(BaseModel):
    ''' articles's author model'''
    name = CharField()
    article = ForeignKeyField(Article, backref = 'authors', on_delete = 'CASCADE', on_update = 'CASCADE')

class Page(BaseModel):
    ''' 页面  model '''
    pass

class Log(BaseModel):
    name = CharField(default = '')
    # 线程开始时间
    start_time = DateTimeField(default = datetime.datetime.now())
    # 线程结束时间
    end_time = DateTimeField(default = '')
    # 线程运行时间
    run_time = DateTimeField(default = 0)
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
