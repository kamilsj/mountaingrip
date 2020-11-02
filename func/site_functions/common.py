from django.contrib.auth.models import User
from start.models import Profile


def check_pic(pic):
    if pic:
        return pic.url
    else:
        return 'https://mountiangrip.s3.amazonaws.com/assets/defaultProfilePicture.jpg'

def check_cover(cover):
    if cover:
        return cover.url
    else:
        return 'https://mountiangrip.s3.amazonaws.com/media/profile/P1000193_B55pk0B.jpg'

def user_id_to_name(user_id):
    user = User.objects.filter(id=user_id).get()
    return user.get_full_name()


def show_user_avatar(user_id, level=0):
    if level == 0:
        user = User.objects.get(id=user_id)
        photo = Profile.objects.get(user_id=user_id)
    else:
        user = User.objects.get(id=user_id)
        photo = Profile.objects.get(user_id=user_id)

    return [user.get_full_name(), check_pic(photo.pic)]


def link_to_html(link):
    pass

