#!/usr/bin/python  
#coding:utf-8
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
import sys
import webbrowser
import codecs
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("./config.conf")
#读取用户全局设置
username = cf.get("globe","username")
password = cf.get("globe", "password")
#登录的主页面  
hosturl = 'http://urp.shou.edu.cn/'
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
posturl = 'http://urp.shou.edu.cn/loginAction.do'   
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
cj = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cj)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  
  
#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
h = urllib2.urlopen(hosturl)  
  
#构造header，一般header至少要包含一下两项。学校抓包数据表明为这两项
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
				   'Referer' : 'http://urp.shou.edu.cn/'}  
#构造Post数据  
postData = {
						'zjh' : username, 
						'mm' : password, 
						}  

print '检验post数据是否正确'
print postData

#需要给Post数据编码  
postData = urllib.urlencode(postData)  
  
#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
request = urllib2.Request(posturl, postData, headers)  
print '校验request是否成功'
print request  
response = urllib2.urlopen(request)  
text = response.read()  
print '校验是否进入学校登陆页面'
print text

##构造get的header，一般header至少要包含一下两项。学校抓包数据表明为这两项
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
				   'Referer' : 'http://urp.shou.edu.cn/menu/s_main.jsp'}
##我们需要get的页面 
geturl = 'http://urp.shou.edu.cn/bxqcjcxAction.do'
request = urllib2.Request(geturl)
#获得返回值
response = urllib2.urlopen(request)  
text = response.read()  
print '校验是否获得目标学分'
#字符串格式转码
text = text.decode('GBK').encode('UTF-8')
#替换计算系统
regex = re.compile("</html>")
upload='<script src="http://apps.bdimg.com/libs/jquery/2.1.1/jquery.min.js"></script><script>function getPoints(t){return t.match("通过")?3.3:t.match("优秀")?3.3:t.match("良好")?2.3:t.match("通过")?1:t>=90?4:t>=85?3.7:t>=82?3.3:t>=78?3:t>=75?2.7:t>=72?2.3:t>=68?2:t>=66?1.7:t>=64?1.5:t>=60?1:0}function getPoint(t,n,r){return sumt=0,suml=0,$.each(t,function(t){0!=t&&(sumt+=r[t]*n[t],suml+=n[t])}),sumt/suml}$(document).ready(function(){var t=new Array,n=new Array,r=new Array;$("#user tr").each(function(e){0!=e&&(r[e]=parseFloat($.trim(this.children[4].innerHTML)),n[e]=$.trim(this.children[6].innerHTML),t[e]=getPoints(n[e]))});var e=getPoint(n,r,t);alert(e)});</script></html>'
text = re.sub(regex,upload,text)
#将文件标示为utf类型
regex = re.compile("<head>")
upload='<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
text = re.sub(regex,upload,text)
print text
#打开文本
# text = unicode(text, "utf-8")
f = open(".\index.html","wt")
#输出到文本
f.write(text)
#关闭文本
f.close()
#打开文件
url = '.\index.html'
webbrowser.open(url)
