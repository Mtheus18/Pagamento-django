from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pagamento
from .services import buscar_pagamentos_cielo

@api_view(["GET"])
def conciliacao_pagamentos(request):

    pagamentos_cielo = buscar_pagamentos_cielo()

    pagamentos_banco = set(
        Pagamento.objects.values_list("transacao", flat=True)
    )

    faltantes = []

    for pagamento in pagamentos_cielo:

        transacao = pagamento.get("Payment", {}).get("PaymentId")
        valor = round(pagamento.get("Payment", {}).get("Amount") / 100,2)
        status = pagamento.get("Payment", {}).get("Status")
        nome = pagamento.get("Payment", {}).get("Name")

        if transacao not in pagamentos_banco and status == 2:

            faltantes.append({
                "transacao": transacao,
                "nome": nome,
                "valor": valor,
                "status": status,
            })

    return Response({
        "total_cielo": len(pagamentos_cielo),
        "total_banco": len(pagamentos_banco),
        "faltantes": len(faltantes),
        "Pagamentos_faltando": faltantes
    })