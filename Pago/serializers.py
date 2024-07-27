from Pago.models import Entidad, Deuda, Cuota
from rest_framework import serializers


class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = ["id", "nombre", "telefono"]


class CuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = ["id", "monto", "fechaVencimiento", "pagada", "voucher"]
        extra_kwargs = {"voucher": {"required": False}, "pagada": {"required": False}}


class DeudaSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(source="userFullName")
    cuotas = CuotaSerializer(many=True)

    class Meta:
        model = Deuda
        fields = [
            "id",
            "usuario",
            "entidad",
            "montoTotal",
            "numeroCuotas",
            "fechaAdquisicion",
            "pagada",
            "cuotas",
        ]
        extra_kwargs = {"pagada": {"required": False}}
