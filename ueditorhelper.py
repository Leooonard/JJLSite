import json
import re

suffixDict= {
      'image': ['jpeg', 'png', 'gif']
}

sizeDict= {
      'image': 2048000
}

def GetUEditorConfig():     
        file= open(r'ueditor/config.json', 'r')
        config= file.read()
        return config

def TestFileType(file, type):
      content_type= file.content_type
      regx= re.compile('^'+ type+ '/')
      if re.search(regx, content_type):
            return True
      else:
            return False

def TestFileSuffix(file, type):
      content_type= file.content_type
      print content_type
      suffixArray= suffixDict[type]
      for suffix in suffixArray:
            regx= re.compile('\/'+ suffix+ '$')
            if re.search(regx, content_type):
                  return True
      return False

def TestFileSize(file, type):
      size= file.size
      max_size= sizeDict[type]
      if size< max_size:
            return True
      else:
            return False

def SaveFile(uploadfile, path):
      name= uploadfile.name
      file= open(path+ name, 'wb+')
      for chunk in uploadfile.chunks():
            file.write(chunk)
      file.close()
      return file

def GetReturnJSON(file, type):
      if type== 'image':
            obj= {
                  'state': 'SUCCESS',
                  'url': '/ueupload/illustration/'+ file.name,
                  'title': file.name,
                  'original': file.name
            }
      else:
            obj= {}
      string= json.write(obj)
      return string