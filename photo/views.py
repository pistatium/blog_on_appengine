from django.shortcuts import render_to_response
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from google.appengine.api import users
from photo import models
from google.appengine.ext.webapp.util import login_required
from django.core.paginator import Paginator
import datetime
datetime.timedelta(hours=9)

class PhotoForm(djangoforms.ModelForm):
    class Meta:
        model = models.Photo
        file  = forms.FileField()

def home(request,page=1):
    q = models.Photo.all().order('-datetime')
    
    if not page: page=1
    #Pager(分割対象,分割数）
    p = Paginator(q, 10).page(page)
    return render_to_response('photo/index.html',{
                                       'photo': p.object_list,
                                       'pager': p,
                                    })
def show(request, photo_id=None):
    photo=models.Photo.get_by_id(int(photo_id))
    response=HttpResponse(photo.image)
    response['Content-Type'] = 'image/jpeg'
    return response
         

def post(request, photo_id=None):
    user=users.get_current_user()
    if not user:
        url=users.create_login_url('/photo/')
        return render_to_response('blog/login.html', {
          'url': url,})
    
    if request.method == 'POST':
        # The form was submitted.
        if photo_id:
            photo = models.Photo.get_by_id(int(photo_id))
            form = PhotoForm(request.POST, instance=photo)
        else:
            # Create a new Book based on the form.
            form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.image = request.FILES["image"].read()
            photo.put()
            if not photo_id: photo_id=photo.key().id()
            
            return HttpResponseRedirect('/photo/')
        # else fail through to redisplay the form with error messages

    else:
        # The user wants to see the form.
        if photo_id:
            # Show the form to edit an existing Book.
            photo = models.Photo.get_by_id(int(photo_id))
            form = PhotoForm(instance=photo)
        else:
            # Show the form to create a new Book.
            form = PhotoForm()

    return render_to_response('photo/post.html', {
        'photo_id': photo_id,
        'form': form,
    })
