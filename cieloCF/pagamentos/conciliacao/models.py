from django.db import models


class Pagamento(models.Model):

    transacao = models.CharField(max_length=100, unique=True)
    nome = models.CharField(max_length=200, db_index=True)

    valor = models.DecimalField(max_digits=10, decimal_places=2)

    data = models.DateTimeField(db_index=True)  # melhor que DateField

    cartao_final = models.CharField(max_length=4, blank=True, null=True)
    bandeira = models.CharField(max_length=20, blank=True, null=True)

    status = models.IntegerField(db_index=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.valor} ({self.transacao})"