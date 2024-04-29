from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Journal(models.Model):
    student = models.CharField(_("ФИО студента"), max_length=100)
    phone_number = PhoneNumberField(
        _("Номер телефона"),
        help_text=_("Пример: +996500123456"),
    )
    date = models.DateField(
        _("Дата заявки"),
        auto_now_add=True,
    )
    is_processed = models.BooleanField(
        _("Статус обработки"),
        default=False,
        help_text=_("Обработано или нет"),
    )
    is_admitted = models.BooleanField(
        _("Поступил к нам"),
        default=False,
        help_text=_("Поступил к нам или нет"),
    )
    comments = models.CharField(
        _("Дополнительные комментарии"), blank=True, null=True, max_length=100
    )

    class Meta:
        verbose_name = _("Журнал")
        verbose_name_plural = _("Записи")
