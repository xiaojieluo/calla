'''
博客生成
'''
import os
from jinja2 import Environment, PackageLoader, FileSystemLoader, PrefixLoader, ChoiceLoader, TemplateNotFound, Undefined
from calla import root
from calla.model import Article
import functools
# class CustomUndefinedError(Undefined):
#     def __init__(self, *args, **kw):
#         pass
class Writer(object):
    def __init__(self, output_path, settings, **kw):
        self.output_path = output_path
        self.settings = settings
        self.init()

    def init(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def write_file(self, filename, context):
        full_path = os.path.join(self.output_path, filename)

        with open(full_path, 'w+') as fp:
            fp.write(context)

class CallaTemplateNotFound(Exception):
    pass

class Generator(object):
    ''' baseclass generator'''
    def __init__(self, config, theme, **kwargs):
        self.config = config
        self.theme = theme
        # self.context = context

        self._templates = {}
        self._templates_path = []
        self._templates_path.append(os.path.expanduser(
            os.path.join(self.theme, 'templates')))

        theme_path = root
        simple_loader = FileSystemLoader(os.path.join(theme_path,
                                         "themes", "default", "templates"))
        self.env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader(self._templates_path),
                simple_loader,  # implicit inheritance
                PrefixLoader({'!simple': simple_loader})  # explicit one
            ]),
            # undefined = CustomUndefinedError
        )

    def generator_page(self, article):
        ''' 生成 page'''
        pass

    def get_template(self, name):
        """Return the template by name.
        Use self.theme to get the templates to use, and return a list of
        templates ready to use with Jinja2.
        """
        if name not in self._templates:
            try:
                self._templates[name] = self.env.get_template(name + '.html')
            except TemplateNotFound:
                raise CallaTemplateNotFound(
                    '[templates] unable to load {}.html from {}'.format(
                        name, self._templates_path))
        return self._templates[name]

class ArticleGenerator(Generator):
    def generate_context(self, article):
        ''' 生成 article
        根据 jinja2 模板生成 html， 返回 html 数据， 由 Writer 类写入
        Args:
            article: dict 类型， 包含文章所有信息
        Return:
            html: str
        '''
        template = self.get_template('article')
        html = template.render(article = article)
        return html

    def generate_output(self, writer):
        for item in Article.select():
            article = item.to_dict()
            html = self.generate_context(article)
            if 'slug' in article:
                filename = '{}.html'.format(article['slug'])
            else:
                filename = '{}.html'.format(article['title'].lower())
            print(filename)

            writer.write_file(filename, html)

class StaticGenerator(Generator):

    def explode_link(self, article):
        link_url = self.config['site']['link_url']
        r = link_url.format(
            id = article['id'],
            year = article['created_at'].year
        )
        return r

    def generate_articles(self, writer):
        template = self.get_template('article')
        for item in Article.select():
            article = item.to_dict()
            filepath = self.explode_link(article)
            article['url'] = self.explode_link(article)
            writer(filepath, template = template, context = {'article': article})

    def generate_author(self, write):
        template = self.get_template('authors')
        all_authors = set()
        for article in Article.select():
            all_authors.add(article.author)

        authors = []
        for author in all_authors:
            articles = Article.select().where(Article.author == author)
            if articles:
                articles = list(articles)
            authors.append((author, articles))

        html = template.render(authors = authors, **self.config)
        write('authors.html', context = self.config, template = template)

    def generate_authors(self, write):
        template = self.get_template('author')
        all_authors = set()
        for article in Article.select():
            all_authors.add(article.author)

        authors = []
        for author in all_authors:
            articles = Article.select().where(Article.author == author)
            if articles:
                articles = list(articles)
            authors.append((author, articles))

        # print(authors)
        for author, articles in authors:
            html = template.render(author = author, **self.config)
            filepath = 'author/{}.html'.format(author)
            write(filepath, template, context = {'author': author})

    def generate_index(self, write):
        ''' 生成首页'''
        template = self.get_template('index')
        write('index.html', template)

    def generate_archives(self, write):
        ''' 生成 Archive'''
        template = self.get_template('archives')
        write('archives.html', template)


    def generate_pages(self, write):
        ''' 生成 page'''
        pass

    def generate_output(self, writer):
        '''
        generate_author
        generate_category
        generate_feeds
        generate_tag
        generate_theme
        '''
        write = functools.partial(writer.write_file)
        writer.output_path = os.path.join(os.getcwd(), self.config.output_path)

        self.generate_articles(write)
        self.generate_author(write)
        self.generate_authors(write)
        self.generate_index(write)
        self.generate_archives(write)
