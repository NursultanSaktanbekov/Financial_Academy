from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.academy.models import Contact
from .models import Journal
from .forms import JournalForm


class JournalListView(View):
    template_name = "journal/journal_list.html"

    def get(self, request):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            journals = Journal.objects.filter(date__range=(start_date, end_date))
        else:
            journals = Journal.objects.all()

        return render(
            request,
            self.template_name,
            {"journals": journals, "displayed_contacts": displayed_contacts},
        )


class AddJournalView(View):
    template_name = "journal/add_journal.html"

    def get(self, request):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        form = JournalForm()
        return render(
            request,
            self.template_name,
            {"form": form, "displayed_contacts": displayed_contacts},
        )

    def post(self, request):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        form = JournalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("journal_list")
        return render(
            request,
            self.template_name,
            {"form": form, "displayed_contacts": displayed_contacts},
        )


class EditJournalView(View):
    template_name = "journal/edit_journal.html"

    def get(self, request, pk):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        journal = get_object_or_404(Journal, pk=pk)
        form = JournalForm(instance=journal)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "journal": journal,
                "displayed_contacts": displayed_contacts,
            },
        )

    def post(self, request, pk):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        journal = get_object_or_404(Journal, pk=pk)
        form = JournalForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect("journal_list")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "journal": journal,
                "displayed_contacts": displayed_contacts,
            },
        )


class StatisticsView(View):
    template_name = "journal/statistics.html"

    def get(self, request, *args, **kwargs):
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            total_applications = Journal.objects.filter(
                date__range=(start_date, end_date)
            ).count()

            processed_applications = Journal.objects.filter(
                is_processed=True, date__range=(start_date, end_date)
            ).count()

            admitted_applications = Journal.objects.filter(
                is_admitted=True, date__range=(start_date, end_date)
            ).count()

            percentage_processed = (
                (processed_applications / total_applications) * 100
                if total_applications > 0
                else 0
            )

            percentage_admitted = (
                (admitted_applications / total_applications) * 100
                if total_applications > 0
                else 0
            )
        else:

            total_applications = Journal.objects.all().count()

            processed_applications = Journal.objects.filter(is_processed=True).count()

            admitted_applications = Journal.objects.filter(is_admitted=True).count()

            percentage_processed = (
                (processed_applications / total_applications) * 100
                if total_applications > 0
                else 0
            )

            percentage_admitted = (
                (admitted_applications / total_applications) * 100
                if total_applications > 0
                else 0
            )

        context = {
            "start_date": start_date,
            "end_date": end_date,
            "total_applications": total_applications,
            "processed_applications": processed_applications,
            "percentage_processed": round(percentage_processed, 2),
            "admitted_applications": admitted_applications,
            "percentage_admitted": round(percentage_admitted, 2),
            "displayed_contacts": displayed_contacts,
        }

        return render(request, self.template_name, context)
