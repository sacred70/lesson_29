
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.viewsets import ModelViewSet
from ads.models import Ad, Category
from ads.serializers import AdSerializer, AdListSerializer, AdDetailSerializer





class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all().order_by("-price")
    serializers = {"list": AdListSerializer, "retrieve": AdDetailSerializer}
    default_serializer = AdSerializer

    def get_serialize_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):

        cat_list = request.GET.getlist("cat")
        if cat_list:
            self.queryset = self.queryset.filter(category_id__in=cat_list)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(authot__locations__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from and price_from.isdigi:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to and price_to.isdigi:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImageView(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse(self.object.serialize())
