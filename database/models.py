#coding= utf-8
from django.db import models

def ImageUploadHandler(instance, filename):
      name= str(instance.path).decode('utf-8').encode('gb2312')
      print 'image/%s'% name
      return 'image/%s'% name

# Create your models here.
class Image(models.Model):
      name= models.CharField(max_length= 50, unique= True)
      date= models.DateField()
      text= models.CharField(max_length= 200)
      path= models.FileField(upload_to= 'image')
      thumb= models.FileField(upload_to= 'thumb', null= True, blank= True)

      def __unicode__(self):
            return self.name


class Blog(models.Model):
      title= models.CharField(max_length= 50, unique= True)
      date= models.DateField()
      sticktop= models.BooleanField(verbose_name= '置顶')
      content= models.TextField()

      def __unicode__(self):
            return self.title

class Illustration(models.Model):
      date= models.DateField()
      path= models.FileField(upload_to= 'illustration')
      blog= models.ForeignKey(Blog, null= True, blank= True, default= None)


class Blogger(models.Model):
      icon= models.FileField(upload_to= 'icon')
      self_introduction= models.TextField(max_length= 500)

      def __unicode__(self):
            return self.self_introduction[:20]