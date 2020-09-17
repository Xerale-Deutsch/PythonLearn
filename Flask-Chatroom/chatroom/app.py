import datetime

import flask
import redis

app = flask.Flask(__name__)
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'
app.config['DEBUG'] = True
rds = redis.StrictRedis()


@app.route('/')
def home():
    """
    主页路由
    如果用户未登录，重定向到登录页
    """

    if 'user' not in flask.session:
        return flask.redirect('/login')
    user = flask.session['user']
    return flask.render_template('home.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录页视图，首次访问需要登录
    """

    if flask.request.method == 'POST':
        # 将用户名存到 session 字典中，重定向到首页
        flask.session['user'] = flask.request.form['user']
        return flask.redirect('/')
    return """
    <form action="" method="post">
        User Name: <input name="user"> 
        <input type="submit" value="login" />
    </form>
    """


def event_stream():
    """
    消息生成器
    在这里创建发布订阅系统，然后再使用发布订阅系统的 subscribe 方法订阅某频道
    """

    pubsub = rds.pubsub()
    pubsub.subscribe('chat')
    for message in pubsub.listen():
        data = message['data']
        if type(data) == bytes:
            yield "data: {0}\n\n".format(data.decode())


@app.route('/post', methods=['POST'])
def post():
    """
    接收JS使用POST发送的数据
    """

    message = flask.request.form['message']
    user = flask.session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()

    rds.publish('chat', '[{0}] {1}: {2}\n'.format(now.isoformat(), user, message))
    return flask.Response(status=204)


@app.route('/stream')
def stream():
    """
    事件流接口
    返回 text/event-stream 类型的对象
    """

    return flask.Response(event_stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)