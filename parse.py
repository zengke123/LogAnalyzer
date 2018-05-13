#!/usr/bin/env python
# encoding: utf-8
# 主程序，对文本进行解析,并输出到对应的文件
import os
from handlers import *
from util import *
from rules import *
from logger import *

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

    def parse(self, file, hostname):
        """
        解析
        """
        self.handler.start('head',hostname)
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

if __name__ == '__main__':
    # file1 = "AS381.201805071050.txt"
    # file2 = "AS382.201805071050 - 副本.txt"
    LogPath = "log" + os.sep
    HtmlPath = "output" + os.sep + "host" + os.sep
    FileList = os.listdir(LogPath)
    handler = HTMLRenderer()
    parser = LogParser(handler)
    for file in FileList:
        hostname = file.split('.')[0]
        output = HtmlPath + hostname + ".html"
        # 开始解析
        with LogSave(output):
            with open(LogPath + file, 'r') as f:
                parser.parse(f, hostname)
