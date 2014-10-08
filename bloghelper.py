#coding= utf-8

from BeautifulSoup import BeautifulSoup
import re

class Bloghelper:
   def initParser(self, html):
      self.soup= BeautifulSoup(html)
      self.max_length= 260

   def getBlogIntroduction(self, html):
      """
            取得导读的规则为: 字数小于260字, 图片若有就放第一张. 如果行数多, 就截取前三行, 但是保证字数小于等于250字.
      """

      # 首先初始化解析器.
      self.initParser(html)
      contents= self.soup.contents
      blogintroductiontext= ''
      for item in contents[0: 3]:
         if len(blogintroductiontext)> self.max_length:
            blogintroductiontext= blogintroductiontext+ ' ... '
            blogintroductiontext= blogintroductiontext+ '<mybr>'          
            break
         blogintroductiontext= blogintroductiontext+ item.text
         if len(blogintroductiontext)> self.max_length:
            blogintroductiontext= blogintroductiontext[0: self.max_length]
            blogintroductiontext= blogintroductiontext+ ' ... '
            blogintroductiontext= blogintroductiontext+ '<mybr>'
            break
         blogintroductiontext= blogintroductiontext+ '<mybr>'
      else:    
         blogintroductiontext= blogintroductiontext+ ' ... '
         blogintroductiontext= blogintroductiontext+ '<mybr>'
      print blogintroductiontext
      blogintroductionimage= ''
      img= self.soup.find('img', src= re.compile('^\/ueupload'))
      if img:
         blogintroductionimage= img.attrMap['src']
      blogintroduction= {
         'text': blogintroductiontext,
         'img': blogintroductionimage
      }
      return blogintroduction

