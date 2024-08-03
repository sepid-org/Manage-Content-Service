from django.urls import path
from .views import get_form_respondents_info, get_form_respondents_answers

urlpatterns = [
    path('form-respondents-info/', get_form_respondents_info,
         name='form_respondents_info'),
    path('form-respondents-answers/',
         get_form_respondents_answers, name='form_respondents_answers'),
]
