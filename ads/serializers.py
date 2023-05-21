import datetime

from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from ads.models import Ad, Category
from users.models import User
from users.serializers import LocationSerializer


class UserAdSerializer(ModelSerializer):
    location = LocationSerializer(many=True)
    age_of_born = SerializerMethodField()

    def get_age_of_born(self, obj):
        return datetime.date.today().year - obj.age

    class Meta:
        model = User
        fields = ["locations", "username", "age_of_born"]


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(ModelSerializer):
    category = SlugRelatedField(slug_field="name", many=True, queryset=Category.objects.all())
    user_locations = SerializerMethodField()

    def get_user_locations(self, obj):
        return [loc.name for loc in obj.author.locations.all()]

    class Meta:
        model = Ad
        fields = ["name", "price", "category", "user_locations"]


class AdDetailSerializer(ModelSerializer):
    author = UserAdSerializer()
    category = SlugRelatedField(slug_field="name", many=True, queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'