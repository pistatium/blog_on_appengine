from django.conf.urls.defaults import *

urlpatterns = patterns('photo.views',
    (r'^post/(\d*)','post'),
    (r'^show/(\d*).jpg','show'),
    (r'^','home'),
)
