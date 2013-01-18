from django import template
from django.template.defaultfilters import stringfilter
import define
register = template.Library()

@register.filter
@stringfilter
def privacy(value):
    return value[:1]+"*"*(len(value)-2)+value[-1]

@register.filter
@stringfilter
def numformat(value):
    i=0
    output=u""
    for line in value.splitlines():
        i+=1
        output+=u"""<span id="lnum">%d</span>%s\n"""%(i,line)
    return output

@register.filter
@stringfilter
def bodyformat(value):
  brFlg=True
  output=""
  if not value: return value
  for line in value.splitlines():
    if line.startswith(u'<pre'):
      brFlg=False
    if line.startswith(u'</pre'):
      brFlg=True
                    
    if brFlg:
        output+=line+"<br>"
    else:
        output+=line+"\n"
  return output

@register.simple_tag
def app_const(attr):
    return getattr(define , attr)
