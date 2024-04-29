from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError


class Contact(models.Model):
    email = models.EmailField(
        _("Электронная почта"), max_length=100, null=True, blank=True
    )
    phone_number = models.CharField(
        _("Номер телефона"), max_length=13, null=True, blank=True
    )
    is_displayed = models.BooleanField(
        _("Отображение на главной странице"), default=False
    )

    instagram = models.URLField(_("Instagram"), max_length=255, null=True, blank=True)
    tiktok = models.URLField(_("TikTok"), max_length=255, null=True, blank=True)
    whatsapp = models.URLField(_("WhatsApp"), max_length=255, null=True, blank=True)
    telegram = models.URLField(_("Telegram"), max_length=255, null=True, blank=True)
    address = models.URLField(_("Адрес"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")

    def __str__(self):
        return self.email

    def clean(self):
        displayed_count = Contact.objects.filter(is_displayed=True).count()
        if self.is_displayed and displayed_count > 1:
            raise ValidationError(
                {
                    "is_displayed": "Нельзя добавить больше 1 отображаемых контактов на главной странице."
                }
            )


class Teacher(models.Model):
    full_name = models.CharField(_("ФИО"), max_length=100)
    experience = models.TextField(_("Опыт"), null=True, blank=True, max_length=1000)
    achievements = models.TextField(_("Награды"), null=True, blank=True)

    is_displayed = models.BooleanField(
        _("Отображение на главной странице"), default=False
    )
    courses = models.ManyToManyField(
        "Course",
        verbose_name=_("Курсы"),
        related_name="teachers",
        blank=True,
    )

    photo = models.ImageField(_("Фотография"), upload_to="teachers/")
    about_me = models.TextField(_("О себе"), null=True, blank=True, max_length=1000)
    role = models.CharField(
        _("Роль"),
        max_length=40,
        null=True,
        blank=True,
    )

    twitter = models.URLField(
        _("Twitter"),
        max_length=255,
        null=True,
        blank=True,
    )
    facebook = models.URLField(
        _("Facebook"),
        max_length=255,
        null=True,
        blank=True,
    )
    instagram = models.URLField(
        _("Instagram"),
        max_length=255,
        null=True,
        blank=True,
    )

    def clean(self):
        displayed_count = Teacher.objects.filter(is_displayed=True).count()
        if self.is_displayed and displayed_count > 5:
            raise ValidationError(
                {
                    "is_displayed": "Нельзя добавить больше 5 отображаемых сотрудников на главной странице."
                }
            )

    class Meta:
        verbose_name = _("Преподаватель")
        verbose_name_plural = _("Преподаватели")

    def __str__(self):
        return self.full_name


class TeacherImage(models.Model):
    images = models.ImageField(_("Изображения"), upload_to="teachers_images/")
    teacher = models.ForeignKey(
        "Teacher",
        verbose_name=_("Преподаватель"),
        related_name="images",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Изображение преподавателя")
        verbose_name_plural = _("Изображения преподавателей")

    def __str__(self):
        return self.teacher.full_name


class Course(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    description = models.TextField(
        _("Описание"),
        null=True,
        blank=True,
    )

    duration = models.CharField(
        _("Длительность (в неделях)"), max_length=100, null=True, blank=True
    )
    number_of_exercises = models.CharField(
        _("Количество занятий"), max_length=100, null=True, blank=True
    )
    number_of_students = models.CharField(
        _("Количество студентов"), max_length=100, null=True, blank=True
    )

    price = models.CharField(_("Цена"), max_length=100, null=True, blank=True)
    visiting_days = models.CharField(
        _("Дни посещения (Пн, Ср, Пт)"), max_length=100, null=True, blank=True
    )
    visiting_time = models.CharField(
        _("Время посещения (12:00-13:00)"), max_length=100, null=True, blank=True
    )

    is_active = models.BooleanField(_("Активен"), default=True)

    trial_lesson = models.URLField(
        _("Пробный урок"), max_length=255, null=True, blank=True
    )
    professional_advantages = models.ManyToManyField(
        "ProfessionalAdvantage",
        verbose_name=_("Профессиональные преимущества курса"),
        blank=True,
    )
    profession = models.CharField(
        _("Профессия"),
        max_length=100,
        null=True,
        blank=True,
    )

    skills = models.TextField(
        verbose_name=_('Список навыков (формат: "навык/. навык/. навык/. ...")'),
        null=True,
        blank=True,
    )
    main_objective = models.TextField(
        _("Главная цель"), null=True, blank=True
    )
    
    badge = models.CharField(
        _("Плашка"), max_length=255, null=True, blank=True,
    )

    @property
    def skills_list(self):
        return [obj.strip() for obj in self.skills.split("/.") if obj.strip()]

    def get_absolute_url(self):
        return reverse("course_detail", args=[str(self.id)])

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")

    def __str__(self):
        return self.name


class ProfessionalAdvantage(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    preview_body = models.CharField(max_length=255, verbose_name=_("Краткое описание"))
    body = models.TextField(verbose_name=_("Текст"))
    logo = models.ImageField(upload_to="advantages/", verbose_name=_("Логотип"))

    class Meta:
        verbose_name = _("Преимущество курса")
        verbose_name_plural = _("Преимущества курса")

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(_("Заголовок"), max_length=100)
    description = models.TextField(_("Описание"))
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")

    def __str__(self):
        return self.title


class NewsImage(models.Model):
    images = models.ImageField(_("Изображения"), upload_to="news/")
    news = models.ForeignKey(
        "News",
        verbose_name=_("Новость"),
        related_name="images",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Изображение новости")
        verbose_name_plural = _("Изображения новостей")

    def __str__(self):
        return self.news.title


class Request(models.Model):
    full_name = models.CharField(_("ФИО"), max_length=100)
    phone_number = models.CharField(_("Номер телефона"), max_length=13)
    email = models.EmailField(
        _("Электронная почта"), max_length=100, null=True, blank=True
    )

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")


class OurService(models.Model):
    image = models.ImageField(_("Картинка"), upload_to="our_services/")
    title = models.CharField(_("Заголовок"), max_length=25)
    description = models.TextField(_("Описание"))
    is_active = models.BooleanField(_("Активен"), default=True)
    is_displayed = models.BooleanField(
        _("Отображение на главной странице"), default=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")

    def clean(self):
        displayed_count = OurService.objects.filter(is_displayed=True).count()
        if self.is_displayed and displayed_count > 3:
            raise ValidationError(
                {
                    "is_displayed": "Нельзя добавить больше 3 отображаемых услуг на главной странице."
                }
            )


class Review(models.Model):
    author = models.CharField(_("Автор"), max_length=100)
    content = models.CharField(_("Содержание"), max_length=255)
    is_displayed = models.BooleanField(
        _("Отображение на главной странице"), default=False
    )

    def clean(self):
        displayed_count = Review.objects.filter(is_displayed=True).count()
        if self.is_displayed and displayed_count > 4:
            raise ValidationError(
                {
                    "is_displayed": "Нельзя добавить больше 4 отображаемых отзывов на главной странице."
                }
            )

    def __str__(self):
        return f"Отзыв от {self.author}"

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")


class Advantage(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    preview_body = models.CharField(max_length=255, verbose_name=_("Краткое описание"))
    body = models.TextField(verbose_name=_("Текст"), max_length=220)
    logo = models.ImageField(upload_to="advantages/", verbose_name=_("Логотип"))
    is_displayed = models.BooleanField(
        _("Отображение на главной странице"), default=False
    )

    def clean(self):
        displayed_count = Advantage.objects.filter(is_displayed=True).count()
        if self.is_displayed and displayed_count > 5:
            raise ValidationError(
                {
                    "is_displayed": "Нельзя добавить больше 5 отображаемых преимуществ на главной странице."
                }
            )

    class Meta:
        verbose_name = _("Преимущество (Практикум)")
        verbose_name_plural = _("Преимущества (Практикум)")

    def __str__(self):
        return self.title


class CompanyHead(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Заголовок"))
    preview_photo = models.ImageField(
        upload_to="company_head_photos/", verbose_name=_("Фотография")
    )
    facts = models.TextField(
        verbose_name=_('Список фактов макс. 4 (формат: "факт/. факт/. факт/. факт/.")')
    )

    @property
    def facts_list(self):
        return [fact.strip() for fact in self.facts.split("/.") if fact.strip()]

    class Meta:
        verbose_name = _("Руководитель компании")
        verbose_name_plural = _("Руководители компании")

    def __str__(self):
        return self.title

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if CompanyHead.objects.exists() and not self.pk:
            raise ValidationError(
                _("Может существовать только один руководитель компании.")
            )


class OutsourcingService(models.Model):
    image = models.ImageField(_("Картинка"), upload_to="our_services/")
    title = models.CharField(_("Заголовок"), max_length=25)
    description = models.CharField(_("Описание"), max_length=255)
    is_displayed = models.BooleanField(
        _("Отображение на главной странице"), default=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Аутсорсинг услуга")
        verbose_name_plural = _("Аутсорсинг услуги")

    def clean(self):
        displayed_count = OutsourcingService.objects.filter(is_displayed=True).count()
        if self.is_displayed and displayed_count > 6:
            raise ValidationError(
                {
                    "is_displayed": "Нельзя добавить больше 6 отображаемых услуг на "
                    "аутсорсинг на главной странице."
                }
            )
