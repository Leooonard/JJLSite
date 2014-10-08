#coding=utf-8

from django.conf.urls.defaults import *
from JJLsite.views import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', Main),
    (r'^main/$', Main),
    (r'^illustration/$', Illustration),
    (r'^bigillustration/(\d+)/(\d+)/$', Bigillustration),
    (r'^blog/$', Blog),
    (r'^bigblog/(\d+)/$', Bigblog),
    (r'^aboutme/$', Aboutme),
    (r'^game/$', Game),
    (r'^search/$', Search),
    (r'^ajaxsearch/$', AjaxSearch),
    (r'^ajaxnextillustration/(\d+)/$', AjaxIllustration, {'prev': False}),
    (r'^ajaxprevillustration/(\d+)/$', AjaxIllustration, {'prev': True}),
    (r'^ajaxblog/(\d+)/$', AjaxBlog),
    (r'^ajaxencode/$', AjaxEncode),
)

backend= patterns('',
    (r'^upload/$', Upload),
    (r'^doupload/$', DoUpload),
)

urlpatterns+= backend

media= patterns('', 
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
    {
        'document_root': settings.STATIC_DIR,
        'show_indexes': True
    }),
)

urlpatterns+= media

ueditor= patterns('',
    (r'^ue/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.UEDITOR_DIR
    }),
    (r'^ueupload/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.UEDITOR_UPDATE_DIR
    }),
    (r'^ueditor/(?P<target>[a-zA-Z]+)/$', UeditorController),
)

urlpatterns+= ueditor

admin= patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^clearCache/$', ClearCache),
    (r'^getCacheIllustrationList/$', GetCacheIllustrationList),
    (r'^deletecacheillitem/(\d+)/$', DeleteCacheIllItem),
)

urlpatterns+= admin


test= patterns('',
    (r'^test/$', Test),
)

urlpatterns+= test


oth= patterns('', 
    (r'^other/$', Other),
    (r'^ajaxother/$', AjaxOther),
)

urlpatterns+= oth

error= patterns('', 
    (r'^.*$', Error404),
)

urlpatterns+= error
