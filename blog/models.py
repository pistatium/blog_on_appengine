from appengine_django.models import BaseModel
from google.appengine.ext import db
from django import test
import datetime
import conf

class Blog(BaseModel):
  title = db.StringProperty(default = "")
  body = db.TextProperty(default = "")
  more = db.TextProperty(default = "")
  tags = db.ListProperty(db.Key)
  category = db.StringProperty(choices=conf.categories)
  datetime = db.DateTimeProperty(auto_now_add = True)
  public = db.BooleanProperty(default = False)
  create_user = db.UserProperty(auto_current_user = True)
  modify_user = db.UserProperty(auto_current_user_add = True)

class BlogReview(BaseModel):
    blog = db.ReferenceProperty(Blog, collection_name='reviews')
    review_author = db.UserProperty()
    review_text = db.TextProperty()
    rating = db.StringProperty(choices=['Poor', 'OK', 'Good', 'Very Good', 'Great'],
                               default='Great')
    create_date = db.DateTimeProperty(auto_now_add=True)

class Tag(BaseModel):
  tag=db.StringProperty()
  @property
  def entries(self):
    return Blog.all().filter('tags',self.key()).order('-datetime')
  
