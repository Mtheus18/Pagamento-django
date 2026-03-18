from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pagamento
from .services import (
    buscar_pagamentos_cielo,
    extrair_dados_pagamento,
    verificar_duplicados_por_criterio,
    STATUS_PAGO
)


@api_view(["GET"])
def conciliacao_pagamentos(request):

    pagamentos_cielo = buscar_pagamentos_cielo()

    pagamentos_banco = set(
        Pagamento.objects.values_list("transacao", flat=True)
    )

    faltantes = []

    dados_processados = []

    for pagamento in pagamentos_cielo:

        dados = extrair_dados_pagamento(pagamento)

        if not dados:
            continue

        dados_processados.append(dados)

        if (
            dados["transacao"] not in pagamentos_banco
            and dados["status"] == STATUS_PAGO
        ):
            faltantes.append({
                "transacao": dados["transacao"],
                "nome": dados["nome"],
                "valor": dados["valor"],
                "cartao_final": dados["cartao_final"],
                "bandeira": dados["bandeira"],
                "titular": dados["titular"],
            })

    duplicados = verificar_duplicados_por_criterio(pagamentos_cielo)

    return Response({
        "total_cielo": len(pagamentos_cielo),
        "total_banco": len(pagamentos_banco),
        "faltantes": len(faltantes),
        "duplicados": len(duplicados),
        "pagamentos_faltando": faltantes,
        "pagamentos_duplicados": duplicados
    })