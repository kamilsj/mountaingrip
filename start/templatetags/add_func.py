from django import template
from func.site_functions import common

register = template.Library()


@register.inclusion_tag('tags/user_avatar.html')
def show_avatar(user_id):
    avatar = common.show_user_avatar(user_id)
    return{
        'name': avatar[0],
        'pic': avatar[1]
    }


@register.inclusion_tag('tags/user_avatar_small.html')
def show_avatar_small(user_id):
    avatar = common.show_user_avatar(user_id)
    return {
        'name': avatar[0],
        'pic': avatar[1]
    }