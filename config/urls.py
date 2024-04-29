from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.academy.sitemaps import CourseSitemap


sitemaps = {
    "courses": CourseSitemap,
}


urlpatterns = (
    [
        path("", include("apps.academy.urls")),
        path("aslan/", admin.site.urls),
        path("account/", include("apps.account.urls")),
        path("journal/", include("apps.journal.urls")),
        path(
            "robots.txt",
            TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        ),
        path(
            "sitemap.xml",
            sitemap,
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)


handler404 = "config.views.page_not_found_view"
