#coding: utf-8
from django.shortcuts import render_to_response
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from google.appengine.api import users
from blog import models
from google.appengine.ext.webapp.util import login_required
from django.core.paginator import Paginator
import conf
import datetime

datetime.timedelta(hours=9)

''' Validation form class '''
class BlogForm(djangoforms.ModelForm):
    class Meta:
        model = models.Blog
        more=forms.TextInput(attrs={'size':'100'})
        exclude = ('tags','users')

def home(request,page):
    login_url,logout_url=_login(request)
    q = models.Blog.all().order('-datetime')
    if not logout_url:
        q.filter("public",True)
    if not page: page=1
    #Pager(分割対象,分割数）
    p = Paginator(q, 10).page(page)
    return render_to_response('blog/index.html',{
                                       'entries': p.object_list,
                                       'pager': p,
                                       'category':conf.categories,
                                       'logout_url':logout_url,
                                       'login_url':login_url,
                                    })

def category(request,category,page):
    q = models.Blog.all().filter("category =",category).order('-datetime')
    if not page: page="/1"
    #Pager(分割対象,分割数）
    p = Paginator(q, 10).page(int(page[1:]))
    return render_to_response('blog/category.html',{
                                       'entries': p.object_list,
                                       'pager': p,
                                       'category':conf.categories
                                    })
def _login(request):
    user=users.get_current_user()
    if not users.is_current_user_admin():
      login_url=users.create_login_url('/')
      logout_url=""
    else:
      login_url=""
      logout_url=users.create_logout_url("/")
    return (login_url,logout_url)

def show(request, entry_id=None):
    if not entry_id:
        return HttpResponseRedirect('/')
    else:
        entry = models.Blog.get_by_id(int(entry_id))
        CAT_NUM=5
        if entry.category:
          q_category = models.Blog.all().filter("category =",entry.category).order('-datetime').fetch(CAT_NUM)
        else:
          q_category = models.Blog.all().order('-datetime').fetch(CAT_NUM)
        dump=entry
        login_url,logout_url=_login(request)
        return render_to_response('blog/show.html', {
          'entry_id': entry_id,
          'entry': entry,
          'category':conf.categories,
          'categories':q_category,
          'logout_url':logout_url,
          'login_url':login_url,
        })
    
def rss(request):
    q = models.Blog.all().order('-datetime')
    import datetime
    return render_to_response('blog/rss.xml',
                              { 'entries': q ,},mimetype="application/rss+xml")

def edit(request, entry_id=None, ajax=False):
    user=users.get_current_user()
    admin=users.is_current_user_admin()
    if not admin:
        return_url = reverse('blog_edit',args=[entry_id,])
        url = users.create_login_url(return_url)
        if ajax:
                return HttpResponse("Not Login")
        else:
          return render_to_response('blog/login.html', {
            'url': url,})
    if request.method == 'POST':
        # The form was submitted.
        if entry_id:
            # Fetch the existing Blog and update it from the form.
            entry = models.Blog.get_by_id(int(entry_id))
            form = BlogForm(request.POST, instance=entry)
        else:
            # Create a new Blog based on the form.
            form = BlogForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.last_user=user
            entry.put()
            if not entry_id: entry_id=entry.key().id()
            
            # ajaxの場合リダイレクトしない
            if ajax:
                return HttpResponse("Success to save.")
            else:
                return_url = reverse('blog.views.show',args=[entry_id,]) 
                return HttpResponseRedirect(return_url)

    else:
        # The user wants to see the form.
        if entry_id:
            # Show the form to edit an existing Blog.
            entry = models.Blog.get_by_id(int(entry_id))
            form = BlogForm(instance=entry)
        else:
            # Show the form to create a new Blog.
            entry = models.Blog(public=False)
            entry.save()
            return_url = reverse('blog_edit',args=[entry.key().id(),])
            return HttpResponseRedirect(return_url)
            #form = BlogForm()

    return render_to_response('blog/edit.html', {
        'entry_id': entry_id,
        'form': form,
    })

