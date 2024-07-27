from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Api.views import EntidadViewSet, DeudaViewSet, UserViewSet, UpdatePassword


router = DefaultRouter()

router.register("entidades", EntidadViewSet)
router.register("deudas", DeudaViewSet)
router.register("users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("update_password/", UpdatePassword.as_view(), name="update_password"),
]
