#coding=utf-8

try:
     import Image
except:
     from PIL import Image
import os

THUMB_WIDTH= 300
THUMB_QUALITY= 75

def GetImagePath(filename):
     return os.getcwd().replace('\\', '/')+ '/upload/image/'+ filename

def GetThumbPath(filename):
     return os.getcwd().replace('\\', '/')+ '/upload/thumb/'+ filename

def RenameFilename(filename, decode= True, Image= True):
     if Image== True:
          path= GetImagePath(filename)
     else:
          path= GetThumbPath(filename)
     if decode== True:
          if Image== True:
               newpath= GetImagePath(filename.decode('utf-8'))
          else:
               newpath= GetThumbPath(filename.decode('utf-8'))
          os.rename(path, newpath)
     else:
          if Image== True:
               oldpath= GetImagePath(filename.decode('utf-8'))
          else:
               oldpath= GetThumbPath(filename.decode('utf-8'))
          print oldpath
          print path
          os.rename(oldpath, path)

def RecodeFilename(filename):
     return filename.decode('utf-8')

def MakeThumb(filename):
     imgpath= GetImagePath(filename)
     thumbpath= GetThumbPath(filename)
     img= Image.open(imgpath)
     width, height= img.size
     # if width<= THUMB_WIDTH:
     if False:
          return None
     else:
          try:
               ratio= width* 1.0/ THUMB_WIDTH
               newHeight= int(height* 1.0/ ratio)
               img= img.resize((THUMB_WIDTH, newHeight), Image.ANTIALIAS)
               img.save(thumbpath, quality= THUMB_QUALITY)
               return 1
          except Exception, e:
               return None

def DeleteThumb(filename):
     thumbpath= GetThumbPath(filename)
     if os.path.isfile(thumbpath):
          os.remove(thumbpath)
          return True
     else:
          return False

def DeleteImage(filename, recode= False, type= None):
     filetype= {
          'image': GetImagePath,
          'thumb': GetThumbPath
     }
     if recode== True:
          # 先重新解码
          filename= RecodeFilename(filename)
     # 获取完整路径
     try:
          path= filetype[type](filename) 
     except:
          path= GetImagePath(filename)
     if not os.path.isdir(path):
          os.remove(path)
          return 1
     else:
          return None
