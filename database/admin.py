#coding= utf-8

from django.contrib import admin
from JJLsite.database.models import *
from JJLsite.utils import RenderResponse
from django.core.exceptions import ObjectDoesNotExist
import os
import thumbhelper

admin.site.register(Blogger)

class ImageAdmin(admin.ModelAdmin):
      def change_view(self, request, object_id, extra_context= None):
            if request.POST:
                  image= Image.objects.get(id= object_id)
                  oldpath= str(image.path)
                  result= super(ImageAdmin, self).change_view(request, object_id, extra_context)
                  image= Image.objects.get(id= object_id)
                  newpath= str(image.path)
                  if oldpath != newpath:
                        # 删除先前的图片.
                        filename= oldpath[6:].lower()
                        # 必须先解码文件名!!!
                        if not thumbhelper.DeleteImage(filename, recode= True, type= 'image'):
                              print  '图片删除'.decode('utf-8')
                              return None
                        if image.thumb:
                              filename= str(image.thumb)[6:].lower()
                              if not thumbhelper.DeleteImage(filename, recode= True, type= 'thumb'):
                                    print '小图标删除'.decode('utf-8')
                                    return None
                        # 为新图片改名字!
                        filename= newpath[6:].lower()
                        filename= thumbhelper.RecodeFilename(filename)
                        thumb= thumbhelper.MakeThumb(filename)
                        if thumb:
                              thumb= 'thumb/'+ filename
                        image.thumb= thumb
                        image.save()
            else:
                  result= super(ImageAdmin, self).change_view(request, object_id, extra_context)
            return result

      def add_view(self, request, form_url= '', extra_context=None):
            if request.POST:
                  name= request.POST.get('name')
                  # 先检查同名图片是否存在.
                  try:
                        img= Image.objects.get(name= name)
                  except:
                        pass
                  else:
                        # 存在说明出错, 直接执行原始逻辑, 并返回出错结果.
                        result= super(ImageAdmin, self).add_view(request, form_url, extra_context)
                        return result
                  # 不存在则添加图片.
                  result= super(ImageAdmin, self).add_view(request, form_url, extra_context)
                  try:
                        # 看是否成功添加. 成功添加则制作缩略图.
                        img= Image.objects.get(name= name)
                        path= str(img.path)
                        filename= path[6:].lower()
                        # 这里帮文件名解码了一下, 使它能正常显示, 所以之后取出文件名也需要做解码操作.
                        filename= thumbhelper.RecodeFilename(filename)
                        thumb= thumbhelper.MakeThumb(filename)
                        if thumb:
                              thumb= 'thumb/'+ filename
                        img.thumb= thumb
                        img.save()
                  except ObjectDoesNotExist, e:
                        # 添加失败, 返回出错结果.
                        return result
                        # from utils import RenderResponse
                        # img= Image.objects.get(name= name)
                        # img.delete()
                        # result= RenderResponse('500.html')
            else:
                  result= super(ImageAdmin, self).add_view(request, form_url, extra_context)
            return result

      def delete_view(self, request, object_id, extra_context=None):
            if request.POST:
                  img= Image.objects.get(id= object_id)
                  path= str(img.path)
                  filename= path[6:].lower()
                  # 一定要解码一次!!!
                  thumbhelper.DeleteImage(filename, recode= True, type= 'image')
                  path= str(img.thumb)
                  filename= path[6:].lower()
                  thumbhelper.DeleteImage(filename, recode= True, type= 'thumb')
            result= super(ImageAdmin, self).delete_view(request, object_id, extra_context)
            return result


admin.site.register(Image, ImageAdmin)

class BlogAdmin(admin.ModelAdmin):
      def myAdmin_ClearSession(self, request):
            if 'ilist' in request.session:
                  ilist= request.session['ilist']
                  for item in ilist:
                        # 找到对应的illustration对象.
                        ill= Illustration.objects.get(id= int(item))
                        # 删除上传的配图.
                        path= ill.path
                        path= os.getcwd().replace('\\', '/')+ '/../upload/'+ path
                        if os.path.isfile(path):
                              os.remove(path)
                        # 删除illustration对象.
                        ill.delete()
                  del request.session['ilist']
      def myAdmin_AddForeignKey(self, request, blog):
            if 'ilist' in request.session:
                  ilist= request.session['ilist']
                  for item in ilist:
                        ill= Illustration.objects.get(id= int(item))
                        ill.blog= blog
                        ill.save()

      def add_view(self, request, form_url= '', extra_context=None):
            if request.POST:
                  title= request.POST.get('title', None)
                  if title== None:
                        result = super(BlogAdmin, self).add_view(request, form_url, extra_context)
                        return result
                  sticktop= request.POST.get('sticktop', False)

                  # 如果该新博客想要置顶, 则不能存在已经置顶的文章.
                  if sticktop:
                        try:
                              blog= Blog.objects.get(sticktop= True)
                        except ObjectDoesNotExist, e:
                              pass
                        else:
                              context= {
                                    'href': 'javascript:void(0);',
                                    'content': '已存在置顶博客!  请按浏览器后退键返回上一页面!'
                              }
                              response= RenderResponse('500.html', context)
                              return response                   

                  # 先判断该博客名是否已存在.
                  try:
                        # 已存在说明出错, 直接退出.
                        blog= Blog.objects.get(title= title)
                  except ObjectDoesNotExist, e:
                        pass
                  else:
                        result = super(BlogAdmin, self).add_view(request, form_url, extra_context)
                        return result

                  # 执行原始函数.
                  result = super(BlogAdmin, self).add_view(request, form_url, extra_context)
                  try:
                        blog= Blog.objects.get(title= title)
                  except ObjectDoesNotExist, e:
                        # 说明添加失败, 直接返回父对象的结果.
                        return result
                  else:
                        # 说明添加成功, 现在需要为session里的项目添加外键, 然后清空session.
                        self.myAdmin_AddForeignKey(request, blog)
                        if 'ilist' in request.session:
                              del request.session['ilist']
            else:
                  result = super(BlogAdmin, self).add_view(request, form_url, extra_context)
            return result

      def change_view(self, request, object_id, extra_context= None):
            if request.POST:
                  title= request.POST.get('title', None)
                  date= request.POST.get('date', None)
                  content= request.POST.get('content', None)
                  if title== None or date== None or content== None:
                        result= super(BlogAdmin, self).change_view(request, object_id, extra_context)
                        return result

                  sticktop= request.POST.get('sticktop', False)
                  blog= Blog.objects.get(title= title)
                  if not blog.sticktop and sticktop:
                        try:
                              sticktopblog= Blog.objects.get(sticktop= True)
                        except ObjectDoesNotExist, e:
                              # 本身不存在置顶对象, 可以置顶.
                              pass
                        else:
                              # 已经存在置顶博客, 出错返回.
                              context= {
                                    'href': 'javascript:void(0);',
                                    'content': '已存在置顶博客!  请按浏览器后退键返回上一页面!'
                              }
                              response= RenderResponse('500.html', context)
                              return response

                  result= super(BlogAdmin, self).change_view(request, object_id, extra_context)
                  try:
                        blog= Blog.objects.get(title= title)
                  except ObjectDoesNotExist, e:
                        # 如果没有取到, 说明修改肯定是失败的. 直接返回父对象的结果.
                        return result
                  else:
                        # 检测对象是否修改成功.
                        newtitle= blog.title
                        newdate= blog.date
                        newcontent= blog.content
                        if title== newtitle and str(date)== str(newdate) and content== newcontent:
                              # 说明修改成功. 可以添加外键然后清空session.
                              self.myAdmin_AddForeignKey(request, blog)
                              if 'ilist' in request.session:
                                    del request.session['ilist']
                        else:
                              # 说明修改失败. 直接返回父对象的结果.
                              return result
            else: 
                  result= super(BlogAdmin, self).change_view(request, object_id, extra_context)
            return result

admin.site.register(Blog, BlogAdmin)