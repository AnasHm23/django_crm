from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.RecordList.as_view(), name='record-list'),
    path('records/<int:pk>', views.RecordRetrieveUpdateDestroy.as_view(), name='record-retrieve-update-destroy'),
    path('records/create/', views.RecordListCreate.as_view(), name='record-create'),
]
