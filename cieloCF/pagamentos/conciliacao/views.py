from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pagamento

from .services import (
    buscar_pagamentos_cielo,
    extrair_dados_pagamento,
    verificar_duplicados_por_criterio,
    filtrar_pagamentos_hoje,
    identificar_faltantes
)


@api_view(["GET"])
def conciliacao_pagamentos(request):

    pagamentos_raw = buscar_pagamentos_cielo()
    pagamentos_hoje = filtrar_pagamentos_hoje(pagamentos_raw)

    pagamentos_banco = set(
        Pagamento.objects.values_list("transacao", flat=True)
    )

    dados_processados = [
        extrair_dados_pagamento(p)
        for p in pagamentos_hoje
    ]

    dados_processados = [d for d in dados_processados if d]

    faltantes = identificar_faltantes(dados_processados, pagamentos_banco)

    duplicados = verificar_duplicados_por_criterio(dados_processados)

    return Response({
        "total_cielo": len(pagamentos_hoje),
        "total_banco": len(pagamentos_banco),
        "faltantes": len(faltantes),
        "duplicados": len(duplicados),
        "pagamentos_faltando": faltantes,
        "pagamentos_duplicados": duplicados
    })