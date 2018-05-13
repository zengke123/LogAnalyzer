#!/usr/bin/env python
# 实现日志输出到对应文件
import logging

formatter = logging.Formatter('%(message)s')
logger = logging.getLogger("test")
logger.setLevel(logging.INFO)

class LogSave():

    def __init__(self,name):
        self.logger = logger
        self.fh = logging.FileHandler(filename=name, mode="w")
        self.fh.setLevel(logging.INFO)
        self.fh.setFormatter(formatter)

    def __enter__(self):
        self.logger.addHandler(self.fh)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.removeHandler(self.fh)