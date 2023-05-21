
from django.urls import path

from ads.views.cat import *

urlpatterns = [
    path('', CategoryListView.as_view()),
    path('<int:pk>', CategoryDitailView.as_view()),
    path('create/', CategoryCreateView.as_view()),
    path('<int:pk>/update/', CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', CategoryDeleteView.as_view())
]
