import json
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer

from users.models import User, Location
from users.serializers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer


class UserPaginator(PageNumberPagination):
    page_size = 4


class UserListView(ListAPIView):
    queryset = User.objects.prefetch_related("location").annotate(total_ads=Count("ad"),
                                                                  filter=Q(ad__is_published=True)).order_by('username')

    serializer_class = UserListSerializer
    pagination_class = UserPaginator


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer


class UserDitailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer












