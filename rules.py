#!/usr/bin/python
# 设计规则来判断每个文本块交给处理程序将要加什么标记

import re

class TitleRule():
    """
    一号标题规则
    """

    def condition(self, block):
        """
        第一行以'<h1>'开头判定为一级标题
        """
        return block[0].startswith('<h1>')

    def action(self, block, handler):
        """
        加标记
        """
        title = block[0].strip('<h1>')
        handler.start('title_h1',title)
        return True

class LogRule():
    """
    日志规则
    """

    def condition(self, block):
        # 第一行以'<log>'开头判定为日志
        return block[0].startswith('<log>')

    def action(self, block, handler):
        title = block[0].strip('<log>')
        handler.start('title_h2',title)
        handler.start('table')
        for i , line in enumerate(block[1:]):
            if i%2 == 0:
                handler.start('tr','even')
            else:
                handler.start('tr', 'odd')
            handler.start('td')
            line = line.replace(" ", "&nbsp;")
            handler.feed(line)
            handler.end('td')
            handler.end('tr')
        handler.end('table')
        handler.end('title_h2')


class TableRule():
    """
    表格规则
    """

    def condition(self, block):
        # 第一行以'<table>'开头判定为表格,且无空行
        # 第一行为二级标题，第二行为表头，第三行开始为表数据
        return block[0].startswith('<table>') and  '' not in block


    def action(self, block, handler):
        title = block[0].strip('<table>')
        handler.start('title_h2',title)
        handler.start('table')
        # 表头
        self.formatTable(block[1:],handler)
        handler.end('table')
        handler.end('title_h2')

    def formatTable(self, block, handler):
        # 取数据按空格分列的最小列数，其他行数据按此列数对齐
        datas = [re.split('[ ]+',line) for line in block]
        # 分列处理后的最小列数
        num = min(len(line) for line in datas)
        finalData = []
        for line in datas:
            point = num - len(line)
            # 将最后多出的列数进行合并
            if point < 0:
                temp_data = line[point-1:]
                line = line[:point-1]
                temp_data = "&nbsp;".join(map(str, temp_data))
                line.append(temp_data)
            finalData.append(line)

        handler.start('tr', 'second_title')
        for data in finalData[0]:
            handler.start('th')
            handler.feed(data)
            handler.end('th')
        handler.end('tr')
        # 表数据
        for i, line in enumerate(finalData[1:]):
            if i % 2 == 0:
                handler.start('tr','even')
            else:
                handler.start('tr', 'odd')
            for data in line:
                handler.start('td')
                handler.feed(data)
                handler.end('td')
            handler.end('tr')


class MixTableRule(TableRule):
    """
    日志与表格混合规则
    """

    def condition(self, block):
        # 第一行以'<table>'开头判定为表格,且日志与表格中间有空行
        return block[0].startswith('<table>') and  '' in block


    def action(self, block, handler):
        title = block[0].strip('<table>')
        handler.start('title_h2',title)
        handler.start('table')
        i = 0
        for i, data in enumerate(block):
            if data == "": break
        for data in block[1:i]:
            handler.start('tr', 'odd')
            handler.start('td')
            handler.feed(data)
            handler.end('td')
            handler.end('tr')
        handler.end('table')
        handler.start('table')
        super().formatTable(block[i+1:],handler)
        handler.end('table')
        handler.end('title_h2')











