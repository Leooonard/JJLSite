#coding= utf-8


from django.template.loader import get_template
from django.template import TemplateDoesNotExist, RequestContext
from django.shortcuts import render_to_response
from  django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from exceptions import NameError, KeyError, UnicodeDecodeError
import json


# 防止模板名错误引起的问题, 错误后导向主页.
def RenderResponse(templateName, context= {}):
    try:
        return render_to_response(templateName, context)
    except TemplateDoesNotExist, e:
        return render_to_response("main.html", {})

def RenderPaginatedResponse(templateName, request, context= {}):
    try:
        return render_to_response(templateName, context, context_instance= RequestContext(request))
    except TemplateDoesNotExist, e:
        return render_to_response('main.html', {})

def RenderRedirect(path):
    return HttpResponseRedirect(path)

def RenderErrorHTML(text= {}):
    try:
        context= {
            'title': text['title'],
            'content': text['content'],
            'href': text['href']
        }
    except(NameError,KeyError), e:
        context= {
            'title': '内部错误',
            'content': '服务器发生小错误啦 %>_<%,  5秒后重定向至我们主页! (⊙o⊙)~~~',
            'href': '/main/'
        }
    finally:
        return RenderResponse('error.html', context)

def RenderTipHTML(text= {}):
    try:
        context= {
            'title': text['title'],
            'content': text['content'],
            'href': text['href']
        }
    # 多个异常时的写法要注意!!!
    except (NameError, KeyError), e:
        context= {
            'title': '内部错误',
            'content': '服务器发生小错误啦 %>_<%,  5秒后重定向至我们主页! (⊙o⊙)~~~',
            'href': '/main/'
        }
    finally:
        return RenderResponse('tip.html', context)

def CompareDate(date1, date2):
    if date1< date2:
        return -1
    elif date1== date2:
        return 0
    elif date1> date2:
        return 1

def WriteObjectToJsonString(obj):
    try:
        return json.write(obj)
    except UnicodeDecodeError, e:
        for item in obj:
            try:
                obj[item]= obj[item].decode('utf-8')
            except Exception, e:
                pass
        return json.write(obj)


def ReadObjectFromJsonString(string):
    return json.read(string)

def PrintArrived(*args):
    print ''
    print '-'* 20+ 'Arrived!!!'+ '-'* 20
    print ''
    for item in args:
        print item
        print '-'* 50
