import pytest
from calla.config import make_config
import os
from calla.generator import  StaticGenerator, ArticleGenerator
from calla.writers import Writer

def generator():
    config = make_config('tests/calla.toml')
    context = config
    # print(config.output_path)
    output_path = os.path.join(os.getcwd(), config.output_path, 'posts')
    writer = Writer(output_path = output_path, settings = config)
    # generator = ArticleGenerator(context = context, theme = config.theme, config = config)
    # generator.generate_output(writer)

    # generate author
    g = StaticGenerator(theme = config.theme, config = config)
    g.generate_output(writer)
