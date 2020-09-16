import datetime
import functools
import os
import re
import urllib

from flask import (Flask, flash, Markup, redirect, render_template, request,
                   Response, session, url_for)
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *

# Blog configuration values.


ADMIN_PASSWORD = 'admin'
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
DEBUG = False
SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz' # Flask App 中加密会话 cookie 的密钥
SITE_WIDTH = 800

app = Flask(__name__)
app.config.from_object(__name__)
flask_db = FlaskDB(app)
database = flask_db.database
oembed_providers = bootstrap_basic(OEmbedCache())


class Entry(flask_db.Model):
    """
    title：标题
    slug：基于标题自动生成的链接地址，可以简单的用 - 把标题里的内容连接在一起
    content：内容（markdown 格式）
    published：是否已发表
    timestamp：创建时间

    save：保存操作，当数据库增加或更新内容时触发，需要更新slug的内容和搜索索引
    update_search_index：创建或更新搜索索引
    html_content: 把 markdown 转化为HTML页面并将多媒体链接转化为HTML内嵌的对象
    search: 全文查找索引
    public: 检索发表的博文
    drafts: 获取所有没公开的博文
    """

    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    @property
    def html_content(self):
        """
        把 markdown 转化为HTML页面并将多媒体链接转化为HTML内嵌的对象
        """
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)

    def save(self, *args, **kwargs):
        """
        保存博文
        """
        if not self.slug:
            self.slug = re.sub('[^\w]+', '-', self.title.lower()).strip('-')
        ret = super(Entry, self).save(*args, **kwargs)

        self.update_search_index()
        return ret

    def update_search_index(self):
        """
        更新索引
        """
        try:
            fts_entry = FTSEntry.get(FTSEntry.entry_id == self.id)
        except FTSEntry.DoesNotExist:
            fts_entry = FTSEntry(entry_id=self.id)
            force_insert = True
        else:
            force_insert = False
        fts_entry.content = '\n'.join((self.title, self.content))
        fts_entry.save(force_insert=force_insert)

    @classmethod
    def public(cls):
        return Entry.select().where(Entry.published == True)

    @classmethod
    def drafts(cls):
        return Entry.select().where(Entry.published == False)

    @classmethod
    def search(cls, query):
        words = [word.strip() for word in query.split() if word.strip()]
        if not words:
            # 返回空串
            return Entry.select().where(Entry.id == 0)
        else:
            search = ' '.join(words)

        return FTSEntry.select(FTSEntry, Entry, FTSEntry.rank().alias('score')).join(Entry, on=(FTSEntry.entry_id == Entry.id).alias('entry')).where((Entry.published == True) & (FTSEntry.match(search))).order_by(SQL('score').desc())


class FTSEntry(FTSModel):
    entry_id = IntegerField(Entry)
    content = TextField()

    class Meta:
        database = database


def login_required(fn):
    """
    由于是单用户模式，不需要多用户的复杂认证，重写个Flask-login
    凡是用到 login_required 的 view 都需要登陆才可以访问。这个
    装饰器通过访问 session 里的 logged_in 字段来判断是否已经登陆。
    """
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))

    return inner


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录视图
    """
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html', next_url=next_url)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    """
    登出视图
    只需要清空 session 并返回登陆页面
    """
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/')
def index():
    """
    博客首页
    """
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())

    return object_list('index.html', query, search=search_query, check_bounds=False)


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    """
    新建博文页面
    需要登录验证
    """
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry = Entry.create(
                title=request.form['title'],
                content=request.form['content'],
                published=request.form.get('published') or False)
            flash('Entry created successfully.', 'success')
            if entry.published:
                return redirect(url_for('detail', slug=entry.slug))
            else:
                return redirect(url_for('edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')
    return render_template('create.html')


@app.route('/drafts/')
@login_required
def drafts():
    """
    博文草稿页面
    需要登录认证
    """
    query = Entry.drafts().order_by(Entry.timestamp.desc())
    return object_list('index.html', query, check_bounds=False)


@app.route('/<slug>/')
def detail(slug):
    """
    博文显示页面
    slug是唯一的，根据slug从数据库中检索得到
    """
    if session.get('logged_in'):
        query = Entry.select()
    else:
        query = Entry.public()
    entry = get_object_or_404(query, Entry.slug == slug)
    return render_template('detail.html', entry=entry)


@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    """
    博文编辑页
    需要登录认证
    """
    entry = get_object_or_404(Entry, Entry.slug == slug)
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry.title = request.form['title']
            entry.content = request.form['content']
            entry.published = request.form.get('published') or False
            entry.save()

            flash('Entry saved successfully.', 'success')
            if entry.published:
                return redirect(url_for('detail', slug=entry.slug))
            else:
                return redirect(url_for('edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')

    return render_template('edit.html', entry=entry)


@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
    """
    为了支持全文搜索,需要添加一个 Jinja 的 Template Filter，
    来过滤掉搜索文字中不需要的内容，保证全文搜索的准确性。
    """
    querystring = dict((key, value) for key, value in request_args.items())
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urllib.urlencode(querystring)


@app.errorhandler(404)
def not_found(exc):
    """
    自定义的404页面
    """
    return Response('<h3>Not found</h3>'), 404


def main():
    database.create_tables([Entry, FTSEntry], safe=True)
    app.run(debug=True)


if __name__ == '__main__':
    main()
