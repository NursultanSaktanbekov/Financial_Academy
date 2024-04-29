from django.contrib.sitemaps import Sitemap

from .models import Course


class CourseSitemap(Sitemap):
    change_freq = "daily"
    priority = 0.5

    def items(self):
        return Course.objects.all()
