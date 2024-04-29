from django.urls import path

from apps.academy.views import (
    IndexView,
    TeacherDetailView,
    CourseDetailView,
    NewsListView,
    TeacherListView,
    ServicesListView,
    CoursesListView,
    ServiceDetailView,
    AccountingView,
    BlankView,
)
from config.settings import BLANK_STARTUP


base_urlpatterns = [
    path(
        "teacher/<int:teacher_id>/", TeacherDetailView.as_view(), name="teacher_detail"
    ),
    path(
        "service/<int:service_id>/", ServiceDetailView.as_view(), name="service_detail"
    ),
    path("course/<int:course_id>/", CourseDetailView.as_view(), name="course_detail"),
    path("news/", NewsListView.as_view(), name="news_list"),
    path("services/", ServicesListView.as_view(), name="services_list"),
    path("courses/", CoursesListView.as_view(), name="courses_list"),
    path("teacher/", TeacherListView.as_view(), name="teacher_list"),
    path("accounting", AccountingView.as_view(), name="accounting"),
]

if BLANK_STARTUP:
    custom_urlpatterns = base_urlpatterns + [
        path("", BlankView.as_view(), name="blank"),
        path("", IndexView.as_view(), name="index"),
    ]
else:
    custom_urlpatterns = base_urlpatterns + [
        path("", IndexView.as_view(), name="index")
    ]
urlpatterns = custom_urlpatterns
