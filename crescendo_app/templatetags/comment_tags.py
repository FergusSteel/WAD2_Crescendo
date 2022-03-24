from django import template
from django.contrib.contenttypes.models import ContentType

from crescendo_app.form import CommentForm
from crescendo_app.models import Comment

register = template.Library()

@register.simple_tag
def get_comment_count(object):
    context_type = ContentType.objects.get_for_model(object)
    return Comment.objects.filter(content_type=context_type,object_id=object.id).count()


@register.simple_tag
def get_comment_form(object):
    context_type = ContentType.objects.get_for_model(object)
    return CommentForm(initial={'content_type': context_type.model, 'object_id': object.id, 'reply_comment_id': 0})


@register.simple_tag
def get_comment_list(object):
    context_type = ContentType.objects.get_for_model(object)
    comments = Comment.objects.filter(content_type=context_type, object_id=object.id, parent=None)
    return comments.order_by('-comment_time')