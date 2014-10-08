#coding= utf-8

from django.http import HttpRequest, HttpResponse
from utils import *
from JJLsite.database.models import *
import datetime
import ueditorhelper


def Main(request):
    response= RenderResponse('main.html')
    return response

def Illustration(request):
    imagelist= Image.objects.order_by('date', 'name')
    context= {
        'imagelist': imagelist,
    }
    response= RenderPaginatedResponse('illustration.html', request, context)
    return response

def Bigillustration(request, id, page):
    try: 
        image= Image.objects.get(id= id)
        context= {
            'image': image,
            'page': page
        }
        response= RenderResponse('bigill.html', context)
    except Exception, e:
        print e
        response= RenderResponse('500.html')
    return response

def AjaxIllustration(request, id, prev):
    from database.models import Image
    import time
    time.sleep(5)
    imagelist= list(Image.objects.order_by('date', 'name'))
    img= Image.objects.get(id= id)
    index= imagelist.index(img)
    # 如果到边界了, 出错返回.
    if not prev:
        if index+ 1== len(imagelist):
            return HttpResponse('failed')
    else:
        if index== 0:
            return HttpResponse('failed')
    # 没到边界, 获取对象, 返回.
    if prev:
        index= index- 1
        img= imagelist[index]
    else:
        index= index+ 1
        img= imagelist[index]
    # 计算页数.
    page= index/ 20+ 1
    obj= {
        'id': img.id,
        'path': str(img.path),
        'text': img.text,
        'page': page
    }
    string= WriteObjectToJsonString(obj)
    PrintArrived(string)
    return HttpResponse(string)

def Blog(request):
    from database import models
    from bloghelper import Bloghelper

    bloghelper= Bloghelper()
    page= request.GET.get('page', None)
    introductionlist= []
    if page:
        page= int(page)
        bloglist= models.Blog.objects.order_by('-sticktop', 'date', 'id')[(page- 1)* 5: page* 5]
    else:
        bloglist= models.Blog.objects.order_by('-sticktop', 'date', 'id')[0: 5]
    for blog in bloglist:
        introductionlist.append(bloghelper.getBlogIntroduction(blog.content))
    bloglist= models.Blog.objects.order_by('-sticktop', 'date', 'id')
    context= {
        'bloglist': bloglist,
        'introductionlist': introductionlist
    }
    response= RenderPaginatedResponse('blog.html', request, context)
    return response

def AjaxBlog(request, id):
    pass

def Bigblog(request, id):
    from database.models import Blog
    id= int(id)
    try:
        blog= Blog.objects.get(id= id)
        bloglist= list(Blog.objects.order_by('-sticktop', 'date', 'id'))
        index= bloglist.index(blog)
        page= index/ 5+ 1
        if index+ 1== len(bloglist):
            nextid= -1
        else:
            nextid= int(bloglist[index+ 1].id)
        if index== 0:
            previd= -1
        else:
            previd= int(bloglist[index- 1].id)
        context= {
            'blog': blog,
            'previd': previd,
            'nextid': nextid,
            'page': page
        }
        response= RenderResponse('bigblog.html', context)
    except:
        response= RenderResponse('500.html')
    return response

def Aboutme(request):
    blogger= Blogger.objects.all()[0]
    print blogger.self_introduction
    response= RenderResponse('aboutme.html', {
        'headphoto': '/ueupload/'+ str(blogger.icon),
        'selfintroduction': blogger.self_introduction
    })
    return response

def Game(request):
    response= RenderResponse('game.html')
    return response

def Upload(request):
    response= RenderResponse('upload.html')
    return response

def DoUpload(request):
    import time
    if(request.method== 'POST'):
        print time.localtime(time.time())
        file= request.FILES.get('file', None)
        print (file.size)
    return RenderRedirect('/upload/')


def UeditorController(request, target):
    print 'UeditorController arrived!!!'
    print target
    action= request.GET.get('action', None)
    if action== 'config':
        config= ueditorhelper.GetUEditorConfig()
        return HttpResponse(config)
    elif action== 'uploadimage':
        '''
            无法应对插入图片之后, 再删除的情况, 服务器会留下这张图片, 当删除相关博文时, 图片会被删除, 否则会在服务器之中.
            需要进行修改.
        '''
        uploadfile= request.FILES.get('upfile', None)
        if not ueditorhelper.TestFileType(uploadfile, 'image'):
            print u'类型错误!'
            return HttpResponse()
        if not ueditorhelper.TestFileSuffix(uploadfile, 'image'):
            print u'后缀错误!'
            return HttpResponse()   
        if not ueditorhelper.TestFileSize(uploadfile, 'image'):
            print u'大小错误!'
            return HttpResponse()

        if target== 'blog':

            # 存数据可的时候会自动存文件, 不用自己再存放一遍.
            # ueditorhelper.SaveFile(uploadfile, 'upload/illustration/')     

            string= ueditorhelper.GetReturnJSON(uploadfile, 'image')
            # 写入数据库.
            # filefield字段接受uploadfile类型数据!!! 也就是在request.files里的数据!!!
            try:
                from database.models import Illustration
                ill= Illustration(date= datetime.date.today(), path= uploadfile)
            except Exception, e:
                print e
            try:
                ill.save()
            except Exception, e:
                print e
            else:
                ilist= request.session.get('ilist', [])
                ilist.append(ill.id)
                request.session['ilist']= ilist
                print request.session['ilist']
            return HttpResponse(string)
    else:
        print action
    return HttpResponse('1')

# 这个函数是为了在使用后台时, 清除不再使用的配图, 若不调用此函数, 配图可能会一直缓存在服务器, 也可能成为错误对象的外键.
def ClearCache(request):
    from JJLsite.database.models import Illustration
    try:
        ilist= request.session.get('ilist', [])
    except:
        ilist= []
    print ilist
    for item in ilist:
        ill= Illustration.objects.get(id= item)
        ill.delete()
    if ilist in request.session:
        del request.session['ilist']
    return HttpResponse('success')

def GetCacheIllustrationList(request):
    from database import models
    if 'ilist' in request.session:
        ilist= request.session['ilist']
        cachelist= []
        deletelist= []
        for item in ilist:
            try:
                ill= models.Illustration.objects.get(id= int(item))
            except Exception, e:
                deletelist.append(item)
                continue

            id= int(item)
            name= str(ill.path)[13:].lower()
            path= '/ueupload/'+ str(ill.path)
            cachelist.append({
                'id': id,
                'name': name,
                'path': path
            })     
        for item in deletelist:
            request.session['ilist'].remove(item)
        if len(request.session['ilist'])== 0:
            del request.session['ilist']
            return HttpResponse('列表为空!')
        string= WriteObjectToJsonString(cachelist)
        return HttpResponse(string)
    else:
        return HttpResponse('列表为空!')

def DeleteCacheIllItem(request, id):
    from database.models import Illustration
    id= int(id)
    try:
        ill= Illustration.objects.get(id= id)
    except ObjectDoesNotExist, e:
        try:
            request.session['ilist'].remove(id)
            if len(request.session['ilist'])== 0:
                del request.session['ilist']
        except:
            return HttpResponse('')
        return HttpResponse('')
    else:
        ill.delete()
        try:
            request.session['ilist'].remove(id)
        except:
            return HttpResponse('')
        else:
            if len(request.session['ilist'])== 0:
                del request.session['ilist']
            return HttpResponse('success')

def Search(request):
    from JJLsite.database import models
    text= request.GET.get('keyword', '')
    fr= request.GET.get('from', 'illustration')
    searchlist= text.split(' ')
    targetContainer= []
    if fr== 'illustration':
        targetContainer= DoSearch(searchlist, models.Image, 'text__icontains')
        for item in DoSearch(searchlist, models.Blog, 'title__icontains'):
            targetContainer.append(item)
    elif fr== 'blog':
        targetContainer= DoSearch(searchlist, models.Blog, 'title__icontains')
        for item in DoSearch(searchlist, models.Image, 'text__icontains'):
            targetContainer.append(item)
    context= {
        'resultlength': len(targetContainer),
        'resultlist': targetContainer
     }       
    return RenderPaginatedResponse('search.html', request, context)

def AjaxSearch(request):
    from JJLsite.database import models
    text= request.GET.get('text', '')
    searchlist= text.split(' ')
    targetContainer= []
    targetContainer= DoSearch(searchlist, models.Image, 'text__icontains')
    targetContainer2= []
    targetContainer2= DoSearch(searchlist, models.Blog, 'title__icontains')
    print 1, targetContainer
    print 2, targetContainer2
    con= zip(targetContainer, targetContainer2)
    con= con[0: 4]
    result= []
    for (i1, i2) in con:
        result.append(i1)
        result.append(i2)
    if len(result)< 8:
        if len(targetContainer)< len(targetContainer2):
            for item in targetContainer2[len(con):]:
                result.append(item)
        elif len(targetContainer)> len(targetContainer2):
            for item in targetContainer[len(con):]:
                result.append(item)
        result= result[0: 8]
    try:
        result= [item.text for item in result]
    except:
        result= [item.title for item in result]
    result= WriteObjectToJsonString(result)
    return HttpResponse(result)

def DoSearch(searchlist, model, field):
    import re
    targetContainer= []
    if not searchlist:
        return targetContainer
    # 首先查找满足所有条件的项.
    condition= {
        field: searchlist[0]
    }
    targetContainer= list(model.objects.filter(**condition))
    for item in searchlist[1: ]:
        condition= {
            field: item
        }
        con= list(model.objects.filter(**condition))
        targetContainer= list(set(con)& set(targetContainer))
    for target in targetContainer:
        text= ''
        for item in searchlist:
            regx= re.compile(u'(^|[^\.,，。 \s]*)'+ item+ u'([^\.,，。 \s]*|$)')
            try:
                t= re.search(regx, target.text).group(0) if re.search(regx, target.text) else 'miss'
            except Exception, e:
                try:
                    t= re.search(regx, target.title).group(0) if re.search(regx, target.title) else 'miss'    
                except:
                    t= 'miss'
            t= t.replace(item, '<mytag>'+ item+ '</mytag>')
            text+= '...'+ t+ ' , '
        try:
            target.text
        except:
            target.title= text
        else:
            target.text= text

    # 接下去是满足单个条件的所有项, 第一个条件的优先级最高!
    for item in searchlist:
        condition= {
            field: item
        }
        con= list(model.objects.filter(**condition))
        for i in con:
            if not i in targetContainer:
                regx= re.compile(u'(^|[^\.,，。 \s]*)'+ item+ u'([^\.,，。 \s]*|$)')
                try:
                    text= re.search(regx, i.text).group(0) if re.search(regx, i.text) else 'miss'
                    i.text= text
                    i.text= i.text.replace(item, '<mytag>'+ item+ '</mytag>')
                except:
                    try: 
                        text= re.search(regx, i.title).group(0) if re.search(regx, i.title) else 'miss'
                        i.title= text
                        i.title= i.title.replace(item, '<mytag>'+ item+ '</mytag>')
                    except:
                        i.text= 'miss'
                targetContainer.append(i)
    return targetContainer

def Error404(request):
    response= RenderResponse('404.html')
    return response

def Error500(request):
    response= RenderResponse('500.html')
    return response

def AjaxEncode(request):
    text= request.GET.get('text', None)
    try:
        text= text.encode('utf-8').encode('gb2312')
    except Exception, e:
        print e
        text= text.decode('gb2312')

    return HttpResponse(text)

def Test(request):
    return RenderResponse('test.html')


def Other(request):
    response= RenderResponse('highcharts.html')
    return response

def AjaxOther(request):
    from BeautifulSoup import BeautifulSoup
    import re
    htmlpath= r'C:\Python25\Lib\site-packages\django\bin\JJLsite\media\html\nbadb.html'.replace('\\', '/')
    content= []
    for line in open(htmlpath, 'r'):
        content.append(line)
    content= ''.join(content)
    soup= BeautifulSoup(content)
    soup= soup.findAll( 'table', attrs= {'class': 'stat_box'})
    soup= BeautifulSoup(str(soup))
    body= soup.findAll(name= 'tbody')
    body= BeautifulSoup(str(body))
    data= []
    for tr in body.findAll('tr'):
        tr= BeautifulSoup(str(tr))
        playerinfo= {}
        playerinfo['name']= getInfo(tr, re.compile('player_name_out'))
        playerinfo['time']= getInfo(tr, re.compile('mp'))
        playerinfo['rebound']= getInfo(tr, re.compile('trb'))
        playerinfo['assist']= getInfo(tr, re.compile('ast'))
        playerinfo['score']= getInfo(tr, re.compile('pts'))
        playerinfo['rate']= getInfo(tr, re.compile('fgper'))
        data.append(playerinfo)
    print data
    head= {
        'name': 'name',
        'y': 'score',
        'drilldown': 'name',
        'id': 'name',
        'dname': ['time', 'rebound', 'assist', 'score', 'rate']
    }
    obj= {
        'head': head,
        'data': data
    }
    return HttpResponse(WriteObjectToJsonString(obj))

def getInfo(tr, regx):
    from BeautifulSoup import BeautifulSoup
    import re
    td= str(tr.findAll(name= 'td', attrs= {'class': regx}))
    td= BeautifulSoup(td)
    if td.findAll(name= 'a'):
        a= str(td.findAll(name= 'a')[0]).decode('utf-8')
    else:
        a= str(td.findAll(True)[0]).decode('utf-8')
    regx= re.compile('>.+<')
    start, end= regx.search(a).span()
    return a[start+ 1: end- 1]