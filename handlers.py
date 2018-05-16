#!/usr/bin/env python
# 为文本块打上 HTML 标记

from logger import logger

class Handler:
    """
    处理程序父类
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method): return method(*args)

    def start(self, name, *args):
        self.callback('start_', name, *args)

    def end(self, name, *args):
        self.callback('end_', name, *args)


class HTMLRenderer(Handler):
    """
    HTML 处理程序,给文本块加相应的 HTML 标记
    """

    def start_title_h1(self, title):
        logger.info('<div class="report_h report_h1">' + str(title) + '</div>\n<div class="report_content">')

    def end_title_h1(self):
        logger.info('</div>')

    def start_title_h2(self,title):
        logger.info('<div class="report_h report_h2">'+ str(title) + '</div>\n<div>')

    def end_title_h2(self):
        logger.info('</div>')

    def start_tr(self,css_name):
        # css_name in (even,odd,second_title)
        logger.info('<tr class="'+ str(css_name) + '">')

    def end_tr(self):
        logger.info('</tr>')

    # def start_th(self, width):
    #     print('<th width=' + str(width)  + '>')

    def start_th(self):
        logger.info('<th>')

    def end_th(self):
        logger.info('</th>')

    def start_td(self, level=None):
        if level is None:
            logger.info('<td>')
        else:
            # level(level_danger_low,level_danger_middle,level_danger_high)分别对应不同的颜色
            logger.info('<td class="' + str(level) + '">')

    def end_td(self):
        logger.info('</td>')

    def start_table(self):
        logger.info('<table class="report_table">')

    def end_table(self):
        logger.info('</table>')

    def feed(self, data):
        logger.info(data)



    def start_head(self,hostname):
        header = '''
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
        <title>主机报表</title>
        <link rel="stylesheet" href="media/report/css/ns_report.css" />
        <link rel="stylesheet" href="media/report/css/ns_report_rsas.css" />
        <script src="media/report/js/jquery-1.7.2.js"></script>
        <script src="media/report/js/common.js"></script>
        <style>pre{}</style>
        </head>
        <body>
	
        <div id="report" class="wrapper">
          <div class="report_tip"></div>
          <div id="head" class="report_title">
            <h1>例检报告-{}</h1>
            <span class="note">&nbsp;</span> 
          </div>
          <!--head end,catalog start-->
          <div id="catalog">
            <div class="report_h1">目录</div>
          </div>
          <div id="content">
        '''.format('{font-size: 13px; font-family: "黑体";}',hostname)
        logger.info(header)

    def end_head(self):
        end_header = '''
        <script type="text/javascript">
	    function getPageY(element){
	  	    return element.offsetTop + (element.offsetParent ? arguments.callee(element.offsetParent) : 0) 
	    }
	    jQuery(function($){
            //window.dialog = new UI.Dialog({name:'dialog'});
            $("#catalog_tree").report_tree();
            $("#report").catalog();
            $('#catalog').delegate('a.link', 'click', function(event){
                event.preventDefault();
                $("#catalog").find("div.report_content").hide();
                $("#catalog").find(".h1_dot").addClass("up");
                jumpToHash(event.target.hash);
            });
            $.gotop();
	    });
        </script>
        </body>
        </html>
        '''
        logger.info(end_header)