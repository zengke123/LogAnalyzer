## LogAnalyzer
将文本日志转换成HTML形式
+  util.py：实现文本块生成器把纯文本分成一个一个的文本块，以便接下来对每一个文本块进行解析
+  handlers.py：为文本块打上合适的 HTML 标记
+  rules.py：规则,用来识别每个文本块交给处理程序将要加什么标记
+  parse.py：对整个日志文本进行解析的程序