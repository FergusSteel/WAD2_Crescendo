from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord

register = template.Library()

@register.simple_tag
def get_like_count(object):
    content_type = ContentType.objects.get_for_model(object)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object.id)
    return like_count.liked_num


@register.simple_tag(takes_context=True)
def get_like_status(context, object):
    content_type = ContentType.objects.get_for_model(object)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=object.id, user=user).exists():
        return 'active'
    else:
        return ''


@register.simple_tag
def get_content_type(object):
    content_type = ContentType.objects.get_for_model(object)
    return content_type.model
