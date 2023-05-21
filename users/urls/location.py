from rest_framework import routers

from users.views import LocationViewSet
router = routers.SimpleRouter()
router.register("", LocationViewSet)
urlpatterns = router.urls
