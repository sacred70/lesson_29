from django.urls import path

from ads.views.ad import *

urlpatterns = [
    path('', AdListView.as_view()),
    path('/<int:pk>', AdDitailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdUploadImageView.as_view())
]
