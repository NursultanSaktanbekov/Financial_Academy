from django.urls import path
from .views import JournalListView, AddJournalView, EditJournalView, StatisticsView


urlpatterns = [
    path("journal_list/", JournalListView.as_view(), name="journal_list"),
    path("journal/add/", AddJournalView.as_view(), name="add_journal"),
    path("journal/edit/<int:pk>/", EditJournalView.as_view(), name="edit_journal"),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
]
