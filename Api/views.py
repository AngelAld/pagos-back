from rest_framework.viewsets import ModelViewSet
from Pago.models import Entidad, Deuda
from Pago.serializers import EntidadSerializer, DeudaSerializer
from Usuario.serializers import UserSerializer, UpdatePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EntidadViewSet(ModelViewSet):
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer
    http_method_names = ["get", "post", "put", "delete"]


class DeudaViewSet(ModelViewSet):
    queryset = Deuda.objects.all()
    serializer_class = DeudaSerializer
    http_method_names = ["get", "post", "put", "delete"]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "put"]


# esto te deslogea
class UpdatePassword(APIView):
    serializer_class = UpdatePasswordSerializer

    def post(self, request):
        password_serializer = UpdatePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if not password_serializer.is_valid():
            return Response(
                password_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.set_password(request.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_200_OK, data={"message": "Password updated"})
