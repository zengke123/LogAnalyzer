#!/usr/bin/env python
# 为文本块打上合适的 HTML 标记

class Handler:
    """
    处理程序父类
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method): return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: result = match.group(0)
            return result
        return substitution

class HTMLRenderer(Handler):
    """
    HTML 处理程序,给文本块加相应的 HTML 标记
    """

    pass

