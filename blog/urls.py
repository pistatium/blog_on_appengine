from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^edit/(\d*)', 'edit',{},'blog_edit'),
    (r'^edit_ajax/(\d*)', 'edit',{'ajax':True},'blog_ajax_edit'),
    (r'^show/(\d*)', 'show'),
    (r'^category/(\w*)(/\d)?', 'category'),
    (r'^rss.xml', 'rss'),
    (r'^(\d)?', 'home'),
)
