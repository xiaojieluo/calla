import pytest
from calla.config import Config
from calla import make_app
import json
from calla.utils import iterdir

@pytest.fixture()
def client(request):
    app = make_app('tests/calla.toml')
    app.config['TESTING'] = True
    client = app.test_client()

    def teardown():
        app.config['TESTING'] = False
    request.addfinalizer(teardown)
    return client

def test_get_all_articles_lists_GET(client):
    url = '/api/articles/'
    res = client.get(url)

    assert res.status_code == 200
    data = res.data.decode('utf-8')
    data = json.loads(data)
    assert isinstance(data, dict)
    assert 'results' in data
    assert 'total' in data
    assert isinstance(data['total'], int)
    assert isinstance(data['results'], list)
