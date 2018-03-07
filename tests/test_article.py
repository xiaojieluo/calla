import markdown
import codecs
from markdown.extensions import meta
import sys
from calla.article import MarkdownArticle, article_factory, Article, InterfaceNotImpleteException
import pytest
import os
from calla.utils import iterdir
from calla.model import Article, Meta
import time
import json
from faker import Faker


@pytest.fixture(scope = 'module')
def init_article_database():
    ''' 生成测试数据'''
    articles = []
    fake = Faker()
    locale = ['zh_CN', 'en_US', 'ru_RU']
    for local in locale:
        for _ in range(10):
            article = {
                'title':'',
                'authors': fake.name(),
                'tags': ','.join([fake.job() * 3]),
                'content': fake.text(),
                'updated_at': fake.time(),
                'bank': fake.iban(),
                'company': fake.company()
            }
            articles.append(article)

    for item in articles:
        Article.create(**item)
        # aid = Article.insert(**item).execute()
        # authors = item.pop('authors')
        # for key, value in metas.items():
        #     Meta.insert(article = aid, key = key, value = value).execute()
        # for author in authors:
        #     Author.insert(article = aid, name = author).execute()

init_article_database()
articles = list(Article.find_all())

@pytest.fixture(params = articles)
def article(request):
    return request.param

def test_article_save():
    article = Article(title = 'Hello', meta = {'test_meta': True})
    article.save()

    vf = Article.find(Article.id == article.id)
    assert vf is not None

    # clean
    test_article_delete(article)
#
def test_article_delete(article):
    article.delete_instance()
    vf = Article.find(Article.id == article.id)
    assert vf is None

def test_get_article_attribute(article):
    assert article.title is not None
    assert article.created_at is not None

def test_article_meta(article):
    meta = article.meta
    for meta in article.meta:
        assert meta.key

def test_article_tags_is_list(article):
    tags = article.to_dict()['tags']
    assert isinstance(tags, list)

def test_article_foreign_meta():
    article = Article(title = 'test_meta')
    article.save()
    meta = Meta(article = article, key = 'slug', value = 'hahha')
    meta.save()

    assert meta.key == 'slug'

    test_article_delete(article)
