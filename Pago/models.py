from django.db import models
from django.contrib.auth.models import User


class Entidad(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Deuda(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.PROTECT)
    montoTotal = models.DecimalField(max_digits=10, decimal_places=2)
    numeroCuotas = models.IntegerField()
    fechaAdquisicion = models.DateField()
    pagada = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def userFullName(self):
        return self.usuario.first_name + " " + self.usuario.last_name

    def __str__(self):
        return (
            self.entidad.nombre
            + " - "
            + str(self.fechaAdquisicion)
            + " - "
            + str(self.montoTotal)
        )


class Cuota(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.PROTECT, related_name="cuotas")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fechaVencimiento = models.DateField()
    pagada = models.BooleanField(default=False)
    voucher = models.ImageField(upload_to="vouchers/", null=True, blank=True)

    def __str__(self):
        return (
            self.deuda.entidad.nombre
            + " - "
            + str(self.fechaVencimiento)
            + " - "
            + str(self.monto)
        )
