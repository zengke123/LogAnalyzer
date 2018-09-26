#!/usr/bin/env python
# encoding: utf-8
# 主程序，对文本进行解析,并输出到对应的文件
# 执行时需要注意环境变量的问题，export LANG=en_US;export LANGUAGE=en_US 会失败
import os
import sys
import datetime
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
        :return: 根据Rule类匹配的告警日志 -> Alarm具名元组
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


    def index(self, CheckTime, HostNum, Alarm):
        '''
        生成index.html
        :param CheckTime: 例检时间
        :param HostNum: 例检主机数量
        :param Alarm: 告警日志,类型为list [(主机名，告警列表),(主机名，告警列表)]
        :return: None
        '''
        self.handler.start("index", CheckTime, HostNum)
        for item in Alarm:
            data = ""
            self.handler.start("tr", "odd")
            self.handler.start("td")
            if len(item[1]) != 0:
                if "level_danger_high" in [alarm.level for alarm in item[1]]:
                    level = "level_danger_high"
                else:
                    level = "level_danger_middle"
                for alarm in item[1]:
                    if alarm.title not in data:
                        data = data + alarm.title + "<br>" + alarm.content +"<br>"
                    else:
                        data = data + alarm.content + "<br>"

            else:
                level = "level_danger_low"
                data = "无异常"
            info = '''
                    <img align='absmiddle' src='host/media/report/images/{}.gif'></img><a href="host/{}.html" target="_blank">{}</a>
                    '''.format(level, item[0], item[0])
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
    # 清理垃圾html文件
    os.system("rm -f output/host/*.html")
    # 需呈现在index中的告警日志,由Rule类匹配，通过Parse类提取并返回
    result = []
    # 生成主机例检报告
    handler = HTMLRenderer()
    for file in file_list:
        parser = LogParser(handler)
        hostname = file.split('.')[0]
        output = html_path + hostname + ".html"
        # 开始解析
        with LogSave(output):
            with open(log_path + file, 'rb') as f:
                # 解析，返回提取到的告警日志
                try:
                    alarms = parser.parse(f, hostname)
                    result.append((hostname,alarms))
                except Exception as e:
                    print(file,e)
    # result按告警严重程序排序
    def paixu(values):
        if len(values) == 0:
            flag = 2
        else:
            if "level_danger_high" in [alarm.level for alarm in values]:
                flag = 0
            else:
                flag = 1
        return flag
    result_sorted = sorted(result, key= lambda item:paixu(item[1]))
    # 生成汇总报告
    host_num = len(file_list)
    check_time = file_list[0].split('.')[1]
    index_parser = LogParser(handler)
    with LogSave("output" + os.sep + "index.html"):
        index_parser.index(check_time,host_num,result_sorted)

    # 输出报告打包
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    os.environ['filename'] = str(filename)
    tar_cmd = 'tar zcf  upfile/report.${filename}.tar.gz output/*'
    os.system(tar_cmd)
    os.system("rm -f log/*.txt")
