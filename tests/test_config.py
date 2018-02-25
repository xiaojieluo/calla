import pytest
from calla.config import make_config, Config
import sys, os
import toml

@pytest.fixture()
def path(request):
    path = os.path.join(os.getcwd(), 'tests/calla.toml')
    return path

@pytest.fixture()
def config(request, path):
    config = make_config(path)
    return config

def test_config_delete(config):
    del config['date_format']['en_us']
    assert 'en_us' not in config['date_format']
    del config['date_format']['not exists']

def test_config_save(config):
    config['date_format']['test_time'] = '%Y'
    config.save()
    reconf = make_config(config._path)
    assert 'test_time' in reconf['date_format']

    #clean
    del config['date_format']['test_time']
    config.save()

def test_config_itemattr(config):
    # get
    assert config['title'] is not None
    assert config['date_format'].zh_cn is not None
    # set
    config['date_format']['test_config_itemattr'] = True
    assert config['date_format']['test_config_itemattr'] is True

def test_config_attribute(config):
    # only get, cannot set attribute
    assert config.title is not None
    assert config.date_format.zh_cn is not None

def test_config_get_method(config):
    assert config.get('title') is not None
    assert config.get('date_format').get('zh_cn') is not None
    assert config.get("not exists", 'Unknow')  == 'Unknow'


def test_config_set_method(config):
    config.test = 'hello'
    assert config.test == 'hello'
