import markdown
import codecs
from markdown.extensions import meta
import sys
from calla.article import MarkdownArticle, article_factory, Article, InterfaceNotImpleteException
import pytest
import os
from calla.utils import iterdir
from calla.model import Article
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
                'author': fake.name(),
                'tags': ','.join([fake.job() * 3]),
                'text': fake.text(),
                'updated_at': fake.time(),
                'meta': { 'bank': fake.iban(), 'company': fake.company() }
            }
            articles.append(article)
    for item in articles:
        Article.create(**item)

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

def test_article_meta_is_dict(article):
    meta = article.meta
    assert isinstance(meta, dict)

def test_article_tags_is_list(article):
    tags = article.tags
    tags = tags.split(',')
    assert isinstance(tags, list)
