class Handler(object):
    """
    文本处理类
    用于打印各种html的标签
    """

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                result = match.group(0)
            return result
        return substitution


class HTMLRender(Handler):
    """
    HTML的处理程序
    给文本块加对应的HTML标记
    """

    def start_document(self):
        print('<html><head><title>此处是标题</title></head><body>')

    def end_document(self):
        print('</body></html>')

    def start_paragraph(self):
        print('<p style="color: #444;">')

    def end_paragraph(self):
        print('</p>')

    def start_heading(self):
        print('<h2 style="color: #68BE5D;">')

    def end_heading(self):
        print('</h2>')

    def start_list(self):
        print('<ul style="color: #363736;">')

    def end_list(self):
        print('</ul>')

    def start_listitem(self):
        print('<li>')

    def end_listitem(self):
        print('</li>')

    def start_title(self):
        print('<h1 style="color: #1ABC9C;">')

    def end_title(self):
        print('</h1>')

    def sub_emphasis(self, match):
        return ('<em>%s</em>' % match.group(1))

    def sub_url(self, match):
        s = ('<a target="_blank" style="text-decoration: none;'
             'color: #BC1A4B;" href="{}">{}</a>')
        return s.format(match.group(1), match.group(1))

    def sub_mail(self, match):
        s = ('<a style="text-decoration: none;color: #BC1A4B;" '
             'href="mailto:{}">{}</a>')
        return s.format(match.group(1), match.group(1))

    def feed(self, data):
        print(data)

