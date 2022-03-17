from django import template
from func.site_functions import common

register = template.Library()


@register.inclusion_tag('tags/user_avatar.html')
def show_avatar(user_id):
    avatar = common.show_user_avatar(user_id)
    return{
        'id': user_id,
        'name': avatar[0],
        'pic': avatar[1]
    }


@register.inclusion_tag('tags/user_avatar_small.html')
def show_avatar_small(user_id):
    avatar = common.show_user_avatar(user_id)
    return {
        'id': user_id,
        'name': avatar[0],
        'pic': avatar[1]
    }

@register.inclusion_tag('tags/user_avatar_public.html')
def show_avatar_public(user_id):
    avatar = common.show_user_avatar(user_id)
    return {
        'id': user_id,
        'name': avatar[0],
        'pic': avatar[1]
    }

@register.filter
def text_to_link(text):
    text = common.text_url_to_html(text)
    return text
