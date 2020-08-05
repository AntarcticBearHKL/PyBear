#coding: UTF-8
import xml.etree.ElementTree as et
import sys,os
sys.path.append('../../../Python/Library')
import Time

def Main(request):
    data = et.fromstring(request.request.body.decode('utf-8'))
    fromstr = data.find('ToUserName').text
    tostr = data.find('FromUserName').text
    print(returnMsg(fromstr, tostr, "hello"))
    request.write(returnMsg(fromstr, tostr, "hello\nddd\nddd"))

def returnMsg(fromstr, tostr, respond):
    return '''
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%d</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content></xml>'''\
    %(tostr, fromstr, Time.Time().toSign(), respond)