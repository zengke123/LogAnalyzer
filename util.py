#!/usr/bin/env python
# 实现文本块生成器把纯文本分成一个一个的文本块，以便接下来对每一个文本块进行解析

def lines(file):
    """
    生成器,在文本最后加一空行
    """
    for line in file: yield line
    yield '\n'

def blocks(file):
    """
    生成器,生成单独的文本块
    以<end>标签作为段落分隔标志

    """
    block = []
    for line in lines(file):
        if not line.startswith("<end>"):
            # 去掉 \n
            line = line.strip('\n')
            # 去除左右两侧的空格
            line = line.lstrip(' ').rstrip(' ')
            block.append(line)
        elif block:
            #yield ''.join(block).strip()
            # 去除文本块前后多余空行
            i = 0
            for i ,data in enumerate(block):
                if data is not "": break
            block = block[i:]
            for i ,data in enumerate(block[::-1]):
                if data is not "": break
            if i != 0:
                block = block[:-i]
            yield block
            block = []




