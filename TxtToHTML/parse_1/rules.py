class Rule(object):
    """
    所有规则类的父类
    """

    def action(self, block, handler):
        """
        加标记
        打印出HTML标签
        """

        handler.start(self.typed)
        handler.feed(block)
        handler.end(self.typed)

        return True


class HeadOneRule(Rule):
    """
    生成h1的规则
    <h1>
    """

    typed = 'title'

    def condition(self, block):
        """
        判断文本块是否符合规则
        返回T或者F
        """
        return "\n" not in block and len(block) <= 70 and not [block][-1] == ':'


class HeadTwoRule(HeadOneRule):
    """
    h2规则
    继承自h1
    """

    typed = 'heading'
    init = True     # 首次调用为T，再次调用为F

    def condition(self, block):
        """
        首次调用后将init改为False
        符合h1规则的，必定符合h2规则，区别只是顺序的区别
        首次调用返回False，即代码块不符合h2规则
        之后调用后返回True
        """

        if not self.init:
            return False
        self.init = False
        return super().condition(block)


class ListItemRule(Rule):
    """
    li规则
    """

    typed = 'listitem'

    def condition(self, block):
        """
        行首为'-'则符合规则
        """

        return block[0] == '-'

    def action(self, block, handler):
        """
        打印li标签
        """
        handler.start(self.typed)
        handler.feed(block[1:].strip())
        handler.end(self.typed)

        return True


class ListRule(ListItemRule):
    """
    ul规则
    """

    typed = 'list'
    inside = False      # 判断是否为列表规则

    def condition(self, block):
        """
        判断代码块是否符合规则这里返回 True
        在 action 方法中调用父类的同名方法再次判断
        """

        return True

    def action(self, block, handler):
        """
        inside 为 False 且 父类的 condition 返回为True时
        打印ul
        """

        if not self.inside and super().condition(block):
            handler.start(self.typed)
            self.inside = True
        elif self.inside and not super().condition(block):
            handler.end(self.typed)
            self.inside = False

        return False


class ParagraphRule(Rule):
    """
    p规则
    """

    typed = 'p'

    def condition(self, block):
        """
        不符合其他规则的按照此规则来处理
        """

        return True


rule_list = [ListRule(), ListItemRule(), HeadTwoRule(), HeadOneRule(), ParagraphRule()]
