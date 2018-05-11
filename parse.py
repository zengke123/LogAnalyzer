# 主程序，对文本进行解析
# encoding: utf-8
import sys
from handlers import *
from util import *
from rules import *


class Parser:
    """
    解析器父类
    """
    def __init__(self, handler):
        self.handler = handler
        self.rules = []

    def addRule(self, rule):
        """
        添加规则
        """
        self.rules.append(rule)

    def parse(self, file):
        """
        解析
        """
        self.handler.start('head')
        first_title_h1 = 0
        for block in blocks(file):
            for rule in self.rules:
                if rule.condition(block):
                    if isinstance(rule,TitleRule):
                        first_title_h1 += 1
                        # 匹配只要不是第一个一级标题，增加</div>结束标签
                        if first_title_h1 !=1 : self.handler.end('title_h1')
                    last = rule.action(block, self.handler)
                    if last: break
        self.handler.end('title_h1')
        self.handler.end('head')


class LogParser(Parser):
    """
    HTML解析器
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(TitleRule())
        self.addRule(LogRule())
        self.addRule(TableRule())
        self.addRule(MixTableRule())

class Logger():
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)


    def flush(self):
        pass

if __name__ == '__main__':
    file = "log/AS381.201805071050.txt"
    # sys.stdout = Logger("output/host/AS381.html")
    with open(file, 'r') as f:
        handler = HTMLRenderer()
        parser = LogParser(handler)
        parser.parse(f)


