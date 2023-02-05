from django.contrib.sitemaps import Sitemap
from apps.groups.models import Thread, ThreadPost, Group


class ThreadPostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ThreadPost.objects.all()

    def lastmod(self, obj):
        return obj.added_at