## LogAnalyzer
将文本日志转换成HTML形式
+  util.py：实现文本块生成器把纯文本分成一个一个的文本块，以便接下来对每一个文本块进行解析
+  handlers.py：为文本块打上合适的 HTML 标记
+  rules.py：规则,用来识别每个文本块交给处理程序将要加什么标记
+  logger.py：控制输出到文件
+  parse.py：主程序，自动解析log目录下所有日志文件、生成html文件，并汇总到index.html,所有html文件存放在output目录下

示例
+ index
![image](https://github.com/zengke123/LogAnalyzer/tree/master/output/demo/index.png)

+ 主机
![image](https://github.com/zengke123/LogAnalyzer/tree/master/output/demo/AS381.png)
