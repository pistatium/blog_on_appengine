from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^photo/', include('photo.urls')),
    (r'^', include('blog.urls')),

)
