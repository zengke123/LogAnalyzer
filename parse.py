#!/usr/bin/env python
# encoding: utf-8
# 主程序，对文本进行解析,并输出到对应的文件
import os
from handlers import *
from util import *
from rules import *
from logger import *
from copy import deepcopy

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
        result = []
        for block in blocks(file):
            for rule in self.rules:
                if rule.condition(block):
                    if isinstance(rule,TitleRule):
                        first_title_h1 += 1
                        # 匹配只要不是第一个一级标题，增加</div>结束标签
                        if first_title_h1 !=1 : self.handler.end('title_h1')
                    rule.action(block, self.handler)

                    # 提取识别到的告警日志
                    if len(rule.alarms) != 0:
                        # 可变对象，需要使用深拷贝
                        temp = deepcopy(rule.alarms)
                        result.extend(temp)
                # 清空告警，避免重复
                rule.clear_alarm()
        self.handler.end('title_h1')
        self.handler.end('head')
        return result


    def index(self,CheckTime, HostNum, Alarm):
        self.handler.start("index", CheckTime, HostNum)
        for k, v in Alarm.items():
            data = ""
            self.handler.start("tr", "odd")
            self.handler.start("td")
            if len(v) != 0:
                if "level_danger_high" in [alarm.level for alarm in v]:
                    level = "level_danger_high"
                else:
                    level = "level_danger_middle"
                for alarm in v:
                    if alarm.title not in data:
                        data = data + alarm.title + "<br>" + alarm.content +"<br>"
                    else:
                        data = data + alarm.content + "<br>"

            else:
                level = "level_danger_low"
                data = "无异常"
            info = '''
                    <img align='absmiddle' src='host/media/report/images/{}.gif'></img><a href="host/{}.html" target="_blank">{}</a>
                    '''.format(level, k, k)
            self.handler.feed(info)
            self.handler.end("td")
            self.handler.start("td")
            self.handler.feed(data)
            self.handler.end("td")
            self.handler.end("tr")
        self.handler.end("index")

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
    LogPath = "log" + os.sep
    HtmlPath = "output" + os.sep + "host" + os.sep
    FileList = os.listdir(LogPath)
    # 需呈现在index中的告警日志,由Rule类匹配，通过Parse类提取并返回
    result = {}
    # 生成主机例检报告
    handler = HTMLRenderer()
    parser = LogParser(handler)
    for file in FileList:
        hostname = file.split('.')[0]
        output = HtmlPath + hostname + ".html"
        # 开始解析
        with LogSave(output):
            with open(LogPath + file, 'r') as f:
                # 解析，返回提取到的告警日志
                alarms = parser.parse(f, hostname)
                result[hostname] = alarms

    # 生成汇总报告
    HostNum = len(FileList)
    CheckTime = FileList[0].split('.')[1]
    with LogSave("output" + os.sep + "index.html"):
        parser.index(CheckTime,HostNum,result)

