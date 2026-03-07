from django.db import models

class Pagamento(models.Model):

    transacao = models.CharField(max_length=100, unique=True)
    nome = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return self.transacao