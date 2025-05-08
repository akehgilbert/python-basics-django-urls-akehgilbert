from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.home, name='home'),
    path('sections/', views.sections_list, name='sections'),
    path('sections/<str:section_name>/', views.section_notes, name='section_notes'),
    path('search/<str:search_term>/', views.search_notes, name='search_notes'),
    path('note/<int:note_id>/', views.note_by_number, name='note_by_number'),
    path('<str:search_term>/', views.search_notes),
]
