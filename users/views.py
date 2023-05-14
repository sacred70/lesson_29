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












@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        locations = data.pop("locations")
        new_user = User.objects.create(**data)
        for loc_name in locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            new_user.locations.add(loc)
        return JsonResponse(new_user.serialize())


class UserDitailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        if "locations" in data:
            locations = data.get("locations")
            self.object.locations.clear()
            for loc_name in locations:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.locations.add(loc)
        if "username" in data:
            self.object.username = data["username"]
        return JsonResponse(self.object.serialize())


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
