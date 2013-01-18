from appengine_django.models import BaseModel
from google.appengine.ext import db
from django import test
import datetime

class Photo(BaseModel):
  image=db.BlobProperty()
  title=db.StringProperty()
  comment=db.StringProperty()
  datetime = db.DateTimeProperty(auto_now_add = True)
