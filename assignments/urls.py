from django.urls import path
from .views import list_assignments, create_assignment, detail, submit, add_objective, answer_objective

urlpatterns = [
    path("", list_assignments, name="list"),
    path("create/", create_assignment, name="create"),
    path("<str:code>/", detail, name="detail"),
    path("<str:code>/submit/", submit, name="submit"),
    path("<str:code>/add-objective/", add_objective, name="add_objective"),
    path("<str:code>/answer-objective/", answer_objective, name="answer_objective"),
]
