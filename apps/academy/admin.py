from django.contrib import admin
from .models import (
    Contact,
    Teacher,
    TeacherImage,
    Course,
    ProfessionalAdvantage,
    News,
    NewsImage,
    Request,
    OurService,
    Review,
    Advantage,
    CompanyHead,
    OutsourcingService,
)


class TeacherImageInline(admin.TabularInline):
    model = TeacherImage
    extra = 3


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [TeacherImageInline]
    list_display = ("full_name", "role", "is_displayed")
    list_filter = ("is_displayed", "courses")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "profession", "is_active")
    list_filter = ("is_active", "teachers", "professional_advantages")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]
    list_display = ("title", "is_active")
    list_filter = ("is_active",)


admin.site.register(Contact)
admin.site.register(Request)
admin.site.register(OurService)
admin.site.register(Review)
admin.site.register(Advantage)
admin.site.register(CompanyHead)
admin.site.register(OutsourcingService)
admin.site.register(ProfessionalAdvantage)
