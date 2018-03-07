from flask import Flask
from calla import make_app

def test_make_app():
    path = 'tests/calla.toml'
    app = make_app(path)

    assert isinstance(app, Flask)
