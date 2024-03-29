from django.contrib.auth.models import User
from start.models import Profile
from func.AI import learn

pic = []
cover = []


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

def get_yt_video_id(url):
    from urllib.parse import urlparse, parse_qs

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError


def text_url_to_html(text):
    from urlextract import URLExtract
    from urllib.parse import urlparse
    extractor = URLExtract()

    urls = extractor.find_urls(text)
    for url in urls:
        if urlparse(url).netloc == 'www.youtube.com':
            text = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+get_yt_video_id(url)+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        elif urlparse(url).netloc == 'youtu.be':
            text = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+get_yt_video_id(url)+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        elif urlparse(url).netloc == 'vimeo.com':
            num_id = urlparse(url).path
            text = text.replace(url, '<iframe src="https://player.vimeo.com/video/' + num_id[1:] + '?h='+num_id[1:]+'" width="560" height="315" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>')
        else:
            text = text.replace(url, '<a href="' + url + '" target="_blank">' + url + '</a>')

    return text
