#!/usr/bin/env python
# encoding: utf-8
# 主程序，对文本进行解析,并输出到对应的文件
import os
import codecs
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
        '''
        解析日志生成html
        :param file: 文件对象
        :param hostname: 主机名
        :return: 根据Rule类匹配的告警日志
        '''
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
        '''
        生成index.html
        :param CheckTime: 例检时间
        :param HostNum: 例检主机数量
        :param Alarm: 告警日志,类型为Dict
        :return: None
        '''
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
    # 日志存放路径
    log_path = "log" + os.sep
    # html文件生成路径
    html_path = "output" + os.sep + "host" + os.sep
    file_list = os.listdir(log_path)
    # 需呈现在index中的告警日志,由Rule类匹配，通过Parse类提取并返回
    result = {}
    # 生成主机例检报告
    handler = HTMLRenderer()
    # parser = LogParser(handler)
    for file in file_list:
        parser = LogParser(handler)
        hostname = file.split('.')[0]
        output = html_path + hostname + ".html"
        # 开始解析
        with LogSave(output):
            with codecs.open(log_path + file, 'rb') as f:
                # 解析，返回提取到的告警日志
                alarms = parser.parse(f, hostname)
                result[hostname] = alarms
    # 生成汇总报告
    host_num = len(file_list)
    check_time = file_list[0].split('.')[1]
    index_parser = LogParser(handler)
    with LogSave("output" + os.sep + "index.html"):
        index_parser.index(check_time,host_num,result)


