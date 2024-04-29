from django import forms

from .models import Journal


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["student", "phone_number", "is_processed", "is_admitted", "comments"]

    def __init__(self, *args, **kwargs):
        super(JournalForm, self).__init__(*args, **kwargs)
        self.fields["phone_number"].error_messages = {
            "invalid": "Введите правильный номер телефона (например, 0312 123 456) или номер с международным префиксом звонка."
        }
