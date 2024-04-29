import datetime


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from apps.academy.models import (
    Teacher,
    Course,
    Contact,
    News,
    TeacherImage,
    OurService,
    Review,
    Advantage,
    CompanyHead,
    OutsourcingService,
)
from .forms import RequestForm
from .sender import send_email


class IndexView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        displayed_teachers = Teacher.objects.filter(is_displayed=True)

        displayed_services = OurService.objects.filter(is_displayed=True)
        active_services = OurService.objects.filter(is_active=True)

        reviews = Review.objects.all()
        displayed_reviews = Review.objects.filter(is_displayed=True)

        advantages = Advantage.objects.all()
        displayed_advantages = Advantage.objects.filter(is_displayed=True)

        contact = Contact.objects.all()
        displayed_contacts = Contact.objects.filter(is_displayed=True)

        company_head = CompanyHead.objects.first()
        courses = Course.objects.all()
        news = News.objects.all()
        form = RequestForm()

        context = {
            "title": "Главная страница",
            "teachers": teachers,
            "displayed_teachers": displayed_teachers,
            "advantages": advantages,
            "displayed_advantages": displayed_advantages,
            "displayed_services": displayed_services,
            "active_services": active_services,
            "reviews": reviews,
            "displayed_reviews": displayed_reviews,
            "contact": contact,
            "displayed_contacts": displayed_contacts,
            "company_head": company_head,
            "courses": courses,
            "form": form,
            "news": news,
        }
        return render(request, "academy/Главная.html", context)

    def post(self, request):
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            current_datetime = datetime.datetime.now()
            formatted_date = current_datetime.strftime("%d.%m.%y")
            formatted_time = current_datetime.strftime("%H:%M")
            message = f"""
    Дата: {formatted_date} | Время: {formatted_time}
    ФИО: {data['full_name']}
    Номер телефона: {data['phone_number']}
    Электронная почта: {data['email']}
            """
            send_email(message)
            return redirect("index")
        return render(request, "academy/Главная.html")


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        contact = Contact.objects.all()
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        form = RequestForm()
        context = {
            "title": f"{teacher.full_name} - преподаватель",
            "teacher": teacher,
            "teachers_images": TeacherImage.objects.all(),
            "contact": contact,
            "form": form,
            "displayed_contacts": displayed_contacts,
        }
        if teacher:
            experience = teacher.experience.split("/")
            achievements = teacher.achievements.split("/")
            context["experience"] = experience
            context["achievements"] = achievements
        return render(request, "academy/teacher_detail.html", context)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        teacher = Teacher.objects.all()
        context = {
            "title": f"{course.name} - курс",
            "course": course,
            "teacher": teacher,
            "displayed_contacts": displayed_contacts,
        }
        return render(request, "academy/Обучение.html", context)


class ServiceDetailView(View):
    def get(self, request, service_id):
        service = get_object_or_404(OurService, id=service_id)
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        context = {
            "title": f"{service.title} - преподаватель",
            "service": service,
            "displayed_contacts": displayed_contacts,
        }
        return render(request, "academy/service_detail.html", context)


class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        context = {
            "title": "Список преподавателей",
            "teachers": teachers,
            "displayed_contacts": displayed_contacts,
        }
        return render(request, "academy/teacher_list.html", context)


class NewsListView(View):
    def get(self, request):
        news = News.objects.filter(is_active=True)
        contact = Contact.objects.filter(is_displayed=True)
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        context = {
            "title": "Список новостей",
            "news": news,
            "contact": contact,
            "displayed_contacts": displayed_contacts,
        }
        return render(request, "academy/news_list.html", context)


class ServicesListView(View):
    def get(self, request):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        displayed_services = OurService.objects.filter(is_displayed=True)
        active_services = OurService.objects.filter(is_active=True)
        context = {
            "title": "Список новостей",
            "displayed_contacts": displayed_contacts,
            "displayed_services": displayed_services,
            "active_services": active_services,
        }
        return render(request, "academy/services_list.html", context)


class CoursesListView(View):
    def get(self, request):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        courses = Course.objects.all()
        context = {
            "title": "Список курсов",
            "courses": courses,
            "displayed_contacts": displayed_contacts,
        }
        return render(request, "academy/courses_list.html", context)


class BlankView(View):
    def get(self, request):
        return render(request, "academy/blank.html")


class AccountingView(View):
    def get(self, request):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        services = OutsourcingService.objects.filter(is_displayed=True)
        contact = Contact.objects.filter(is_displayed=True)
        context = {
            "title": f"Аутсорсинг Бухгалтерии",
            "contact": contact,
            "services": services,
            "displayed_contacts": displayed_contacts,
        }
        return render(request, "academy/accounting.html", context)
